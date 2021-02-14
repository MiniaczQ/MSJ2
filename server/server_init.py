'''
Initialization of server class.
'''

from os import getcwd, path, getenv
import sys
import threading
from shlex import split
import asyncio as aio

import server_files
from server_names import names
from settings import settings


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

java_path = getenv('JAVA') or getenv('JAVA_HOME') or getenv('JAVA_PATH')

class Server():
    def __init__(self, id):
        '''
        Creates the instance's folder by copying the template.
        '''
        self.id = id
        self.directory = path.join(getcwd(), names[id])
        self.change_state(States.Offline)
        self.process = None
        self.reader = aio.Event()

        server_files.copy_template(self.directory)
        server_files.set_properties(self.directory, {
            'server-ip': '127.0.0.1',
            'server-port': settings['local_ports_start'] + id,
            'motd': settings['motd'].replace('@name', names[id]),
            'level-name': 'world',
            'level-seed': '' 
        })

        self.args = split(settings['java_arguments'])
        self.args.insert(0, path.join(java_path, 'bin', 'java.exe'))
        self.args.append('-jar')
        self.args.append(settings['server_jar_name'])
        if settings['nogui']:
            self.args.append('--nogui')
    
    def __del__(self):
        '''
        Deletes the copy of the template.
        '''
        server_files.delete_template_copy(self.directory)