
from os import getcwd, path

import server_files
from server_names import names

states_decoder = (
    "Offline",      #   0
    "Starting",     #   1
    "Generating",   #   2
    "Awaiting",     #   3
    "Probing",      #   4
    "Prioritized"   #   5
)

class States:
    Offline = 0
    Starting = 1
    Generatong = 2
    Awaiting = 3
    Probing = 4
    Prioritized = 5

states_decoder = dict((value, key) for key, value in States.__dict__.items() if not key.startswith('__') and not callable(key))

class Server:
    def __init__(self, manager, id):
        self.id = id
        self.directory = path.join(getcwd(), names(id))
        self.change_state(States.Offline)
        self.process = None

        server_files.copy_template(self.directory)

    def reset(self):
        server_files.delete_ops(self.directory)
        server_files.delete_whitelist(self.directory)
        server_files.delete_world(self.directory)
    
    def change_state(self, new_state):
        '''
        Called when server state changes
        '''
        self.state = new_state
        #   TODO    Tell discord bot to update

    def start(self):
        '''
        Start a process.\n
        Start output reading coroutine.
        '''
        self.change_state(States.Starting)
        pass

    def stop(self):
        '''
        Stop a process.\n
        Stop output reading coroutine.
        '''
        self.change_state(States.Offline)
        pass

    def world_store(self, seed):
        server_files.store_world(self.directory, seed)

    def __del__(self):
        server_files.delete_template(self.directory)