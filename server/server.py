import sys
import asyncio as aio

from server_listener import Server





#   Testing

if __name__ == '__main__':
    from time import sleep

    if sys.platform == 'win32':
        loop = aio.ProactorEventLoop()
        aio.set_event_loop(loop)

    async def test():
        s = Server(1)
        l = aio.Lock()

        await s.start()

        await l.acquire()
        await l.acquire()
        
        await s.stop()
    
    loop.run_until_complete(test())