'''
Server input interface.
'''

import asyncio as aio
import sys

from server_states import States

class ServerInput:
    async def write(self, msg):
        '''
        Writes to the server console.
        '''
        self.process.stdin.write((msg + '\n').encode())
        await self.process.stdin.drain()

    def reset(self):
        '''
        Deletes world, whitelist and server operators from the server.
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
        Called after '/seed' is used.\n
        Stores the world with the seed as a name.
        '''
        self.store_world(seed)

    async def start(self):
        '''
        Starts the server process.
        '''
        if self.process is not None:
            await self.process.wait()
        self.reset()
        if self.process is None:
            self.process = await aio.subprocess.create_subprocess_exec(*self.args, stdin=aio.subprocess.PIPE, stdout=aio.subprocess.PIPE, cwd=self.directory)
            self.start_reader()

    async def stop(self):
        '''
        Stops the server process.
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
        self.set_properties({
            'server-ip': self.ip,
            'server-port': self.port,
            'motd': self.motd,
            'level-name': 'world',
            'level-seed': '',
            'view-distance': self.view_distance
        })
    
    def call_manager(self, coroutine):
        self.manager.call_async(coroutine)

    def call_redirector(self, coroutine):
        self.manager.redirection_manager.call_fat(coroutine)