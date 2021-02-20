'''
Finalization of manager class.
'''

import asyncio as aio
from time import sleep, monotonic
from collections import deque

from server import Server
import aio_loops

from manager_files import ManagerFiles
from manager_input import ManagerInput
from manager_output import ManagerOutput
from manager_states import States

class Manager(ManagerFiles, ManagerInput, ManagerOutput, aio_loops.LoopBase):
    def __init__(self, redirection_manager, logging, startup_time, directory, templates_path, server_count, ip, port_start, servers_path, worlds_path, jarname, motd='%(name)s', javargs='', nogui=False, view_distance=16):
        self.state = self.change_state(States.Stopped)
        self.loop = aio_loops.ManagerLoop

        self.redirection_manager = redirection_manager
        
        self.logging = logging
        self.directory = directory

        self.templates_path = templates_path

        self.server_count = server_count
        self.servers = []

        self.templates = self.get_all_templates()
        self.template = None

        self.ip = ip
        self.port_start = port_start
        self.servers_path = servers_path
        self.worlds_path = worlds_path
        self.jarname = jarname
        self.motd = motd
        self.javargs = javargs
        self.nogui = nogui
        self.view_distance = view_distance

        self.average_startup_time = 12
        self.cycle_again_callback = None

        self.prioritized = None

        self.offline_queue = deque()
        self.not_empty_queue = aio.Event()





#   Testing

if __name__ == '__main__':
    async def test():
        from os import getcwd, path
        from logging_config import logging
        from unittest.mock import Mock

        root = getcwd()

        l = aio.Lock()

        m = Manager(Mock(), logging, 12, root, path.join(root, 'templates'), 2, '192.168.1.2', 25566, path.join(root, 'servers'), path.join(root, 'worlds'), 'fabric-server-launch.jar')

        m.change_template('1.16.1f')
        await m.start()

        await l.acquire()
        await l.acquire()
        
        await m.stop()
    
    aio_loops.ManagerLoop.run_until_complete(test())