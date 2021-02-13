#   Define lööps ┌('▽')┐

import asyncio as aio
from threading import Thread

DiscordLoop = aio.new_event_loop()
ManagerLoop = aio.new_event_loop()
RedirectorLoop = aio.new_event_loop()

class DiscordThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        aio.set_event_loop(DiscordLoop)

class ManagerThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        aio.set_event_loop(ManagerLoop)

class RedirectorThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        aio.set_event_loop(RedirectorLoop)