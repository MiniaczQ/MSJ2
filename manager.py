'''
Finalization of manager class.
'''

import asyncio as aio
from time import sleep, monotonic

from settings import settings
from server import Server

#   Enum for states
class States:
    Stopped = 0
    Cycling = 1
    Priority = 2

#   Inverse mapping (states_decoder[state_id] => state_name)
states_decoder = dict((value, key) for key, value in States.__dict__.items() if not key.startswith('__') and not callable(key))

class Manager():
    def __init__(self):
        self.state = States.Stopped
        self.event = aio.Event()
        for id in range(settings['server_count']):
            self.servers.append(Server(id))

    def start(self):
        '''
        Start the manager.\n
        Sequentially launch servers.\n
        Actively change the redirection.
        '''
        self.state = States.Cycling
        self.event.set()
        aio.ensure_future(self.start())
    
    def run(self):
        '''
        Prevent 
        '''
        

    def stop(self):
        '''
        Stop all servers and all redirectors.
        '''
        self.event.clear()
        self.state = States.Stopped

    def __del__(self):
        '''
        Cleanup.
        '''
        del self.servers





#   Testing

if __name__ == '__main__':
    manager = Manager()
    manager.start()

    input()

    manager.stop()