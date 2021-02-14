'''
Definition of all needed loops and threads.
'''

import asyncio as aio
from threading import Thread

DiscordLoop = aio.new_event_loop()
ManagerLoop = aio.new_event_loop()
RedirectorLoop = aio.new_event_loop()

class DiscordThread(Thread):
    pass

class ManagerThread(Thread):
    pass

class RedirectorThread(Thread):
    pass