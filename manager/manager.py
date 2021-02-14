#   States, main server loop

import threading
from time import sleep, monotonic

from settings import settings
from server_core import Server
from redirector import Redirector
from logger import logger

#   Enum for states
class States:
    Stopped = 0
    Cycling = 1
    Priority = 2

#   Inverse mapping (states_decoder[state_id] => state_name)
states_decoder = dict((value, key) for key, value in States.__dict__.items() if not key.startswith('__') and not callable(key))

class Manager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.state = States.Stopped
        self.servers = []
        self.redirectors = []
        self.current_redirector = None
        self.interval = 10.0
        self.ready_servers = 0
        for id in range(settings['server_count']):
            self.servers.append(Server(id))
            self.redirectors.append(Redirector(settings['local_ports_start'] + id, settings['visible_port']))

    def start(self):
        '''
        Start the manager.\n
        Sequentially launch servers.\n
        Actively change the redirection.
        '''
        self.state = States.Cycling
        threading.Thread.start(self)
    
    def run(self):
        '''
        Don't run this method.\n
        Use 'start' instead!
        '''
        while self.state > 0:
            logger.info('Server started')
            sleep(self.interval)

    def stop(self):
        '''
        Stop all servers and all redirectors.
        '''
        self.state = States.Stopped

    def __del__(self):
        '''
        Cleanup.
        '''
        del self.servers

    def change_redirector(self, new_redirector_id):
        '''
        Start the new redirector.\n
        Stop previous, if there was one.\n
        None to stop all redirectors.
        '''
        if self.current_redirector is not None:
            self.redirectors[self.current_redirector].stop()
        
        if new_redirector_id is not None:
            self.current_redirector = new_redirector_id
            self.redirectors[self.current_redirector].start()





#   Testing

if __name__ == '__main__':
    manager = Manager()
    manager.start()

    input()

    manager.stop()