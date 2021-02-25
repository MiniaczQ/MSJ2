'''
Server input interface.
'''

import asyncio as aio
import sys

from server_states import States

class ServerInput:
    async def write(self, msg):
        '''
        Coroutine.\n
        Write to server.
        '''
        self.process.stdin.write((msg + '\n').encode())
        await self.process.stdin.drain()

    def reset(self):
        '''
        Delete world, whitelist, ops.\n
        Reset class variables.\n
        Update properties.
        '''
        self.delete_ops()
        self.delete_whitelist()
        self.delete_world()
        self.players.clear()
        self.enforce_properties()
        self.player_count = 0
        self.op = None
        self.advancements.clear()
        self.start_time = None

    def change_state(self, new_state):
        '''
        Call to change server state.
        '''
        if States.validate(new_state):
            self.state = new_state
            self.state_changed(new_state)

    def store_world(self, seed):
        '''
        Stores the world with the seed as a name.
        '''
        self.store_world(seed)

    async def start(self):
        '''
        Coroutine.\n
        Start the server process.
        '''
        if self.process is not None:
            await self.process.wait()
        self.reset()
        if self.process is None:
            self.process = await aio.subprocess.create_subprocess_exec(*self.args, stdin=aio.subprocess.PIPE, stdout=aio.subprocess.PIPE, cwd=self.directory)
            self.start_reader()

    async def stop(self):
        '''
        Coroutine.\n
        Stop the server process.
        '''
        if self.process is not None:
            self._stop('')
            self.stop_reader()
            self.process.terminate()
            await self.process.wait()
            self.process = None
    
    def start_reader(self):
        '''
        Start server console reader.
        '''
        self.reader.set()
        self.call_async(self.read_loop())
    
    def stop_reader(self):
        '''
        Stop server console reader.
        '''
        self.reader.clear()

    def enforce_properties(self):
        '''
        Update server properties.
        '''
        self.set_properties({
            'server-ip': self.ip,
            'server-port': self.port,
            'motd': self.motd,
            'level-name': 'world',
            'level-seed': '',
            'view-distance': self.view_distance,
            'spawn-protection': 0
        })
    
    def call_manager(self, coroutine):
        '''
        Call manager's coroutine.
        '''
        self.manager.call_async(coroutine)

    def call_redirector(self, coroutine):
        '''
        Call redirector's coroutine.
        '''
        self.manager.redirection_manager.call_fat(coroutine)