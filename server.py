'''
Finalization of server class.
'''

import sys
import asyncio as aio
from shlex import split
from os import path, getenv

import server_files
import server_input
import server_output
import server_states
import server_names

_java_path = getenv('JAVA') or getenv('JAVA_HOME') or getenv('JAVA_PATH')

class Server():
    def _assemble_args(self, javargs, jarname, nogui):
        self.args = split(javargs)
        self.args.insert(0, path.join(_java_path, 'bin', 'java.exe'))
        self.args.append('-jar')
        self.args.append(jarname)
        if nogui:
            self.args.append('--nogui')
    
    def _set_properties(self, ip, port, motd):
        server_files.set_properties(self, {
            'server-ip': ip,
            'server-port': port,
            'motd': motd.replace('%(name)s', server_names.names[self.id]),
            'level-name': 'world',
            'level-seed': '' 
        })

    def __init__(self, logging, id, ip, port, servers_path, template_path, worlds_path, jarname, motd='%(name)s', javargs='', nogui=False):
        '''
        Creates the instance's folder by copying the template.
        '''
        self.logging = logging

        self.id = id
        self.name = server_names.names[id]
        self.directory = path.join(servers_path, self.name)
        self.change_state(server_states.States.Offline)
        self.process = None
        self.reader = aio.Event()

        self.template_path = template_path
        self.worlds_path = worlds_path

        server_files.copy_template(self)
        self._set_properties(ip, port, motd)
        self._assemble_args(javargs, jarname, nogui)

        self.players = {}
        self.advancements = {}
    
    def __del__(self):
        '''
        Deletes the copy of the template.
        '''
        server_files.delete_template_copy(self)
    
    #   Loading i/o methods
    write = server_input.write
    reset = server_input.reset
    change_state  = server_input.change_state
    store_world = server_input.store_world
    start = server_input.start
    stop = server_input.stop

    start_reader = server_output.start_reader
    read = server_output.read
    stop_reader = server_output.stop_reader





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
        s = Server(logging, 0, '192.168.1.2', 25566, path.join(root, 'servers'), path.join(root, 'template'), path.join(root, 'worlds'), 'fabric-server-launch.jar')
        l = aio.Lock()

        await s.start()

        await l.acquire()
        await l.acquire()
        
        await s.stop()
    
    loop.run_until_complete(test())