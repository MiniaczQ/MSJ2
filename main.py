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
        manager = Manager(redirector,
                          logging,
                          hidden_settings.startup_time,
                          cwd,
                          path.join(cwd, hidden_settings.templates_path),
                          settings['server_count'],
                          settings['server_ip'],
                          settings['local_ports_start'],
                          path.join(cwd, hidden_settings.servers_path),
                          path.join(cwd, hidden_settings.worlds_path),
                          settings['server_jar_name'],
                          settings['motd'],
                          settings['java_arguments'],
                          settings['nogui'],
                          16)
        manager.change_template(settings['default_template'])
        manager.call_async(manager.start())
        aio_loops.ManagerLoop.run_forever()

class RedirectorThread(aio_loops.RedirectorThread):
    def run(self):
        aio.set_event_loop(aio_loops.RedirectorLoop)
        global redirector
        redirector = RedirectionManager(settings['server_ip'],
                                        list(settings['local_ports_start'] + i for i in range(settings['server_count'])),
                                        settings['visible_port'],
                                        hidden_settings.packet_size)
        
        mt = ManagerThread()
        mt.start()

        aio_loops.RedirectorLoop.run_forever()

def main():
    #dt = DiscordThread()
    rt = RedirectorThread()
    rt.start()

if __name__ == '__main__':
    main()