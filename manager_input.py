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
        self.template = None
        if new_template in self.templates:
            self.create_servers_folder()
            for id in range(self.server_count):
                self.servers.append(Server(self, self.logging, id, self.ip, self.port_start + id, self.servers_path, path.join(self.directory, self.template), self.worlds_path, self.jarname, self.motd, self.javargs, self.nogui))
            self.template = new_template

        self.logging.info(f'Template changed to {self.template}.')

    async def start(self):
        '''
        Start the cycler.
        '''
        self.change_state(States.Cycling)

    async def stop(self):
        '''
        Stop the cycler.
        '''
        self.change_state(States.Stopped)