'''
Finalization of server class.
'''

import sys
import asyncio as aio
from shlex import split
from os import path, getenv

from server_files import ServerFiles
from server_input import ServerInput
from server_output import ServerOutput
from server_states import States
from server_names import names

_java_path = getenv('JAVA') or getenv('JAVA_HOME') or getenv('JAVA_PATH')

class Server(ServerFiles, ServerInput, ServerOutput):
    def _assemble_args(self, javargs, jarname, nogui):
        self.args = split(javargs)
        self.args.insert(0, path.join(_java_path, 'bin', 'java.exe'))
        self.args.append('-jar')
        self.args.append(jarname)
        if nogui:
            self.args.append('--nogui')
    
    def _set_properties(self, ip, port, motd):
        self.set_properties({
            'server-ip': ip,
            'server-port': port,
            'motd': motd.replace('%(name)s', names[self.id]),
            'level-name': 'world',
            'level-seed': '' 
        })

    def __init__(self, manager, logging, id, ip, port, servers_path, template_path, worlds_path, jarname, motd='%(name)s', javargs='', nogui=False):
        '''
        Creates the instance's folder by copying the template.
        '''
        self.manager = manager
        self.logging = logging

        self.id = id
        self.name = names[id]
        self.directory = path.join(servers_path, self.name)
        self.change_state(States.Offline)
        self.process = None
        self.reader = aio.Event()

        self.template_path = template_path
        self.worlds_path = worlds_path

        self._set_properties(ip, port, motd)
        self._assemble_args(javargs, jarname, nogui)

        self.players = {}
        self.advancements = {}

        self.server_start_time = None
        self.speedrun_start_time = None





#   Testing

if __name__ == '__main__':
    from time import sleep

    if sys.platform == 'win32':
        loop = aio.ProactorEventLoop()
        aio.set_event_loop(loop)

    async def test():
        from os import getcwd
        from logging_config import logging

        root = path.join('..', getcwd())
        s = Server(logging, 0, '192.168.1.2', 25566, path.join(root, 'servers'), path.join(root, 'templates', '1.16f'), path.join(root, 'worlds'), 'fabric-server-launch.jar')
        l = aio.Lock()

        await s.start()

        await l.acquire()
        await l.acquire()
        
        await s.stop()
    
    loop.run_until_complete(test())