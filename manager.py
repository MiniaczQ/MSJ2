'''
Finalization of manager class.
'''

import asyncio as aio
from time import sleep, monotonic

from server import Server

from manager_files import ManagerFiles
from manager_input import ManagerInput
from manager_output import ManagerOutput
from manager_states import States

class Manager(ManagerFiles, ManagerInput, ManagerOutput):
    def __init__(self, logging, directory, templates_path, server_count, ip, port_start, servers_path, worlds_path, jarname, motd, javargs, nogui):
        self.state = self.change_state(States.Stopped)
        
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





#   Testing

if __name__ == '__main__':
    manager = Manager()
    manager.start()

    input()

    manager.stop()