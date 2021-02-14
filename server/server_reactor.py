'''
Operations on the server.
'''

import asyncio as aio
import sys

import server_files
import server_init
from server_init import States
import settings

class Server(server_init.Server):
    def start_reader(self):
        pass
    
    def stop_reader(self):
        pass

    def write(self, msg):
        '''
        Writes to the server console.
        '''
        self.process.write(msg)

    def reset(self):
        '''
        Deletes world, whitelist and server operators from the server.
        '''
        server_files.delete_ops(self.directory)
        server_files.delete_whitelist(self.directory)
        server_files.delete_world(self.directory)

    def change_state(self, new_state):
        '''
        Called when server state changes.
        '''
        self.state = new_state
        #   TODO    Tell discord bot to update
        #aio.run_coroutine_threadsafe()

    def world_store(self, seed):
        '''
        Called when '/seed' is used.\n
        Stores the world with the seed as a name.
        '''
        server_files.store_world(self.directory, seed)

    async def start(self):
        '''
        Starts the server process.
        '''
        if self.process is None:
            self.process = await aio.subprocess.create_subprocess_exec(*self.args, stdin=aio.subprocess.PIPE, stdout=aio.subprocess.PIPE, cwd=self.directory)

            self.start_reader()

            self.change_state(States.Starting)

    async def stop(self):
        '''
        Stops the server process.
        '''
        if self.process is not None:
            self.stop_reader()

            self.process.terminate()
            await self.process.wait()
            self.process = None

            self.change_state(States.Offline)