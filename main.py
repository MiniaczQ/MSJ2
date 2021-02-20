'''
Execution of modules on different threads.
'''

import asyncio as aio
from os import getcwd, path

from logging_config import logging
import aio_loops
#from discordbot_core import discordbot_start
from redirection_manager import RedirectionManager
from manager import Manager
from settings import settings
import hidden_settings

redirector = None
manager = None

class DiscordThread(aio_loops.DiscordThread):
    def run(self):
        aio.set_event_loop(aio_loops.DiscordLoop)
        #discordbot_start()

class ManagerThread(aio_loops.ManagerThread):
    def run(self):
        aio.set_event_loop(aio_loops.ManagerLoop)
        global manager, redirector
        cwd = getcwd()
        manager = Manager(redirector, logging, 12, cwd, path.join(cwd, 'templates'), 2, '192.168.1.2', 25566, path.join(cwd, 'servers'), path.join(cwd, 'worlds'), 'fabric-server-launch.jar')
        manager.change_template('1.16.1f')
        manager.call_async(manager.start())
        aio_loops.ManagerLoop.run_forever()

class RedirectorThread(aio_loops.RedirectorThread):
    def run(self):
        aio.set_event_loop(aio_loops.RedirectorLoop)
        global redirector
        redirector = RedirectionManager('192.168.1.2', (25566, 25567), 25565, 2**16)
        
        mt = ManagerThread()
        mt.start()

        aio_loops.RedirectorLoop.run_forever()

def main():
    #dt = DiscordThread()
    rt = RedirectorThread()
    rt.start()

if __name__ == '__main__':
    main()