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
    def call(self, coroutine):
        '''
        Untracked execution called from another thread.
        '''
        self.loop.call_soon_threadsafe(coroutine)
        aio.SelectorEventLoop().call_soon_threadsafe

    def ensure(self, coroutine):
        '''
        Untracked execution called from the same thread.
        '''
        aio.ensure_future(coroutine, loop=self.loop)

    def later(self, delay, coroutine):
        '''
        Tracked execution after specified delay called from the same thread.
        '''
        return self.loop.call_later(delay, coroutine)