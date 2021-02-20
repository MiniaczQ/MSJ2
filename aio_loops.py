'''
Definition of all needed loops and threads.
'''

import asyncio as aio
from threading import Thread
import sys

DiscordLoop = aio.new_event_loop()
if sys.platform == 'win32':
    ManagerLoop = aio.ProactorEventLoop()
else:
    ManagerLoop = aio.new_event_loop()
RedirectorLoop = aio.new_event_loop()

class DiscordThread(Thread):
    pass

class ManagerThread(Thread):
    pass

class RedirectorThread(Thread):
    pass

class LoopBase:
    def call_fat(self, coroutine):
        '''
        Call an async function from another thread (loop).
        '''
        aio.run_coroutine_threadsafe(coroutine, loop=self.loop)

    def call_async(self, coroutine):
        '''
        Call an async function in the same thread (loop).
        '''
        return self.loop.create_task(coroutine)