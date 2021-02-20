'''
Manager input interface.
'''

import asyncio as aio
from os import path

from manager_states import States
from server import Server

class ManagerInput:
    def change_state(self, new_state):
        '''
        Call to change manager state.
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

        self.servers.clear()
        self.offline_queue.clear()
        self.template = None
        if new_template in self.templates:
            self.template = new_template
            self.logging.info(f'Template changed to {self.template}.')
            self.create_servers_folder()
            for id in range(self.server_count):
                server = Server(self, self.logging, id, self.ip, self.port_start + id, self.servers_path, path.join(self.templates_path, self.template), self.worlds_path, self.jarname, self.motd, self.javargs, self.nogui, self.view_distance)
                server.copy_template()
                self.servers.append(server)
                self.offline_queue.append(server)
        self.not_empty_queue.set()

    async def start(self):
        '''
        Start the manager.\n
        Start in cycling mode.
        '''
        self.change_state(States.Cycling)
        self.call_async(self.cycle())

    async def stop(self):
        '''
        Stop the manager.\n
        Stops all servers.\n
        Cancels both cycling and priority mode.
        '''
        self.cycle_again_callback.cancel()
        self.change_state(States.Stopped)
    
    async def update_average_startup_time(self, delta):
        self.average_startup_time = self.average_startup_time * 0.9 + delta * 0.1
        self.logging.info(f'Startup time between servers updated to {self.average_startup_time:0.3f} seconds.')
    
    async def cycle(self):
        '''
        Launch a server and schedule another cycle call in the future.
        '''
        await self.not_empty_queue.wait()
        server = self.offline_queue.popleft()
        if len(self.offline_queue) == 0:
            self.not_empty_queue.clear()
        await server.start()
        self.logging.info(f'Attempting to start server {server.name}.')
        await aio.sleep(self.average_startup_time)
        self.cycle_again_callback = self.call_async(self.cycle())
            
    async def prioritize(self, server):
        '''
        Enables priority mode on the manager.\n
        Stops all but the selected server.\n
        Cancels next scheduled cycle.
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
        Disables priority mode on the manager.\n
        Stops the prioritized server.\n
        Restarts server cycling.
        '''
        if server == self.prioritized:
            self.change_state(States.Cycling)
            self.logging.info(f'Deprioritizing server {server.name}, returning to cycling.')
            self.prioritized = None
            self.cycle_again_callback = self.call_async(self.cycle())
    
    def call_server(self, coroutine):
        self.call_async(coroutine)
    
    def server_killed(self, server):
        self.offline_queue.append(server)
        self.not_empty_queue.set()