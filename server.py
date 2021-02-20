'''
Finalization of server class.
'''

import sys
import asyncio as aio
from shlex import split
from os import path, getenv

import aio_loops

from server_files import ServerFiles
from server_input import ServerInput
from server_output import ServerOutput
from server_states import States
from server_names import names

_java_path = getenv('JAVA') or getenv('JAVA_HOME') or getenv('JAVA_PATH')

class Server(ServerFiles, ServerInput, ServerOutput, aio_loops.LoopBase):
    def _assemble_args(self, javargs, jarname, nogui):
        self.args = split(javargs)
        self.args.insert(0, path.join(_java_path, 'bin', 'java.exe'))
        self.args.append('-jar')
        self.args.append(jarname)
        if nogui:
            self.args.append('--nogui')

    def __init__(self, manager, logging, id, ip, port, servers_path, template_path, worlds_path, jarname, motd='%(name)s', javargs='', nogui=False, view_distance=16):
        '''
        Creates the instance's folder by copying the template.
        '''
        self.manager = manager
        self.logging = logging
        self.loop = aio_loops.ManagerLoop

        self.id = id
        self.port = port
        self.name = names[id]
        self.directory = path.join(servers_path, self.name)
        self.ip = ip
        self.motd = motd.replace('%(name)s', self.name)
        self.view_distance = view_distance
        
        self.process = None
        self.reader = aio.Event()

        self.template_path = template_path
        self.worlds_path = worlds_path

        self._assemble_args(javargs, jarname, nogui)

        self.player_count = 0
        self.players = {}
        self.advancements = {}

        self.server_start_time = None
        self.speedrun_start_time = None

        self.change_state(States.Offline)





#   Testing

if __name__ == '__main__':
    import threading
    from os import getcwd
    from logging_config import logging
    from unittest.mock import Mock
    
    server = None

    async def test():
        root = getcwd()
        global server
        server = Server(Mock(), logging, 0, '192.168.1.2', 25566, path.join(root, 'servers'), path.join(root, 'templates', '1.16.1f'), path.join(root, 'worlds'), 'fabric-server-launch.jar')
        server.copy_template()
        server.enforce_properties()
        l = aio.Lock()

        await server.start()
    
    def console():
        while True:
            msg = input()
            server.call_fat(server.write(msg))

    threading._start_new_thread(console, ())

    aio_loops.ManagerLoop.create_task(test())

    aio_loops.ManagerLoop.run_forever()