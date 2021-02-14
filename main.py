'''
Execution of modules on different threads.
'''

import asyncio as aio

import main_init as base
from discordbot_core import discordbot_start
from redirection_manager import RedirectionManager

redirector = None

class DiscordThread(base.DiscordThread):
    def run(self):
        aio.set_event_loop(base.DiscordLoop)
        discordbot_start()

class ManagerThread(base.ManagerThread):
    def run(self):
        aio.set_event_loop(base.ManagerLoop)

class RedirectorThread(base.RedirectorThread):
    def run(self):
        aio.set_event_loop(base.RedirectorLoop)
        global redirector
        redirector = RedirectionManager('192.168.1.2', (25566, 25567), 25565, 2**16)

def main():
    DiscordThread.start()
    ManagerThread.start()
    RedirectorThread.start()

if __name__ == '__main__':
    main()