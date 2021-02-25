'''
Input interface for the manager class.
'''

import asyncio as aio
from os import path

from manager_states import States
from server import Server

class ManagerInput:
    def change_state(self, new_state):
        '''
        Changes the current state of the manager.
        '''
        if States.validate(new_state):
            self.state = new_state
            self.state_changed(new_state)

    def change_template(self, new_template):
        '''
        Change the previous template to a new one.\n
        Create new servers using the new template.\n
        If new one is invalid, only deletes the previous ones.
        '''
        if self.template is not None:
            self.delete_servers_folder()

        self.template = None
        self.servers.clear()
        self.offline_queue.clear()

        if new_template in self.templates:
            self.template = new_template
            self.create_servers_folder()
            for id in range(self.server_count):
                server = Server(self, self.logging, id, self.ip, self.port_start + id, self.servers_path, path.join(self.templates_path, self.template), self.worlds_path, self.jarname, self.motd, self.javargs, self.nogui, self.view_distance)
                server.copy_template()
                self.servers.append(server)
                self.offline_queue.append(server)

            self.logging.info(f'Template changed to {self.template}.')
        self.not_empty_queue.set()
    
    def call_server(self, coroutine):
        '''
        Call server's coroutine.
        '''
        self.call_async(coroutine)

    async def start(self):
        '''
        Coroutine.\n
        Start the manager in cycling mode.
        '''
        self.call_async(self.cycle())

        self.change_state(States.Cycling)

    async def stop(self):
        '''
        Coroutine.\n
        Stop the manager and all servers.
        '''
        self.cycle_again_callback.cancel()

        self.change_state(States.Stopped)
    
    async def update_average_startup_time(self, delta):
        '''
        Coroutine.\n
        Updates the average start time for servers.
        '''
        self.average_startup_time = self.average_startup_time * 0.9 + delta * 0.1
    
    async def start_next_server(self):
        '''
        Coroutine.\n
        Attempts to start the next server in queue.\n
        Waits if queue is empty.
        '''
        await self.not_empty_queue.wait()
        server = self.offline_queue.popleft()
        if len(self.offline_queue) == 0:
            self.not_empty_queue.clear()
        
        await server.start()

        self.logging.info(f'Attempting to start server {server.name}.')
    
    async def cycle(self):
        '''
        Coroutine.\n
        Launch a server and schedule another start in the future.
        '''
        server = await self.start_next_server()

        self.cycle_again_callback = self.call_async(self.delayed_cycle())

    async def delayed_cycle(self):
        '''
        Coroutine.\n
        Wait for the average start time, then launch a server.
        '''
        await aio.sleep(self.average_startup_time)
        await self.cycle()
            
    async def prioritize(self, server):
        '''
        Coroutine.\n
        Enable priority mode on the manager.\n
        Stop all but the prioritized server.\n
        Cancel next scheduled server launch.
        '''
        self.prioritized = server

        self.cycle_again_callback.cancel()
        for s in self.servers:
            if s != server:
                self.call_server(s.stop())

        self.change_state(States.Priority)
        self.logging.info(f'Prioritizing server {server.name}, killing all other servers.')

    async def deprioritize(self, server):
        '''
        Coroutine.\n
        Disable priority mode on the manager and return to cycling.\n
        Stop the prioritized server.\n
        Schedule start of the next server.
        '''
        if server != self.prioritized:
            return
        
        self.prioritized = None
        self.cycle_again_callback = self.call_async(self.cycle())

        self.change_state(States.Cycling)
        self.logging.info(f'Deprioritizing server {server.name}, returning to cycling.')