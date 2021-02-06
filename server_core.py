from os import getcwd, path, listdir
import sys

import asyncio as aio
from shlex import split

import server_files
from server_names import names
from settings import settings

from os import getenv

java_path = getenv('JAVA') or getenv('JAVA_HOME') or getenv('JAVA_PATH')

#   Enum for states
class States:
    Offline = 0
    Starting = 1
    Generatong = 2
    Awaiting = 3
    Probing = 4
    Prioritized = 5
    Speedrunning = 6

#   Inverse mapping (states_decoder[state_id] => state_name)
states_decoder = dict((value, key) for key, value in States.__dict__.items() if not key.startswith('__') and not callable(key))

class Server:
    def __init__(self, manager, id):
        '''
        Creates the instance's folder by copying the template.
        '''
        self.id = id
        self.directory = path.join(getcwd(), names[id])
        self.change_state(States.Offline)
        self.process = None

        server_files.copy_template(self.directory)
    
    def __del__(self):
        '''
        Deletes the copy of the template.
        '''
        server_files.delete_template_copy(self.directory)

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
        args = split(settings['java_arguments'])
        args.insert(0, path.join(java_path, 'bin', 'java.exe'))
        args.append('-jar')
        args.append(settings['server_jar_name'])
        if settings['nogui']:
            args.append('--nogui')
        cmd = ''.join(arg + ' ' for arg in args)

        if self.process is not None:
            self.process.kill()

        self.process = await aio.subprocess.create_subprocess_exec(*args, stdin=aio.subprocess.PIPE, stdout=aio.subprocess.PIPE, cwd=self.directory)

        self.change_state(States.Starting)

    async def stop(self):
        '''
        Stops the server process.
        '''
        if self.process is not None:
            self.process.terminate()
            self.process = None

        self.change_state(States.Offline)
        




#   Testing

if __name__ == '__main__':
    from time import sleep

    if sys.platform == 'win32':
        loop = aio.ProactorEventLoop()
        aio.set_event_loop(loop)
    
    loop = aio.get_event_loop()
    s = Server('manager', 1)

    loop.run_until_complete(s.start())

    input()

    loop.run_until_complete(s.stop())

    input()