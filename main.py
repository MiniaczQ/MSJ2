'''
Execution of modules on different threads.
'''

import asyncio as aio

import main_init as base
from discordbot_core import discordbot_start

class DiscordThread(base.DiscordThread):
    def run(self):
        discordbot_start()

class ManagerThread(base.ManagerThread):
    def run(self):
        pass

class RedirectorThread(base.RedirectorThread):
    def run(self):
        pass

def main():
    DiscordThread.start()
    ManagerThread.start()
    RedirectorThread.start()

if __name__ == '__main__':
    main()