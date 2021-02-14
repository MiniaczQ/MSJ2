import logging
from collections import deque

from redirector import Redirector

class RedirectionManager():
    def __init__(self, ip, ports_to, port_from, packet_size):
        '''
        Class for managing local port redirecting.\n
        Redirects one port to one from multiple.\n
        Arguments:\n
        ip          -   Server machine IP (on the network you port forward)\n
        ports_to    -   Ports to redirect to (ports of the servers)\n
        port_from   -   Port to redirect from (port the people use)\n
        packet_size -   Bytes per data transfer (preferably power of 2)
        '''
        self.redirectors = {}
        for port_to in ports_to:
            self.redirectors[port_to] = Redirector(ip, port_to, port_from, packet_size)
        self.current = None
        self.queue = deque()
    
    def validate_port(self, port):
        return port if port in self.redirectors.keys() else None

    async def change(self, new):
        '''
        Changes the current redirector.\n
        If the new port is invalid only stops the previous redirector.
        '''
        if self.current is not None:
            await self.redirectors[self.current].stop()
        
        self.current = None
        if new in self.redirectors.keys():
            await self.redirectors[new].start()
            self.current = new

        logging.info(f'Redirection changed to {self.current}')

    async def append(self, port):
        '''
        Add a port to the redirection queue.\n
        If it's the first element in the queue, it will be used.\n
        Otherwise it will be used when it reaches the front of the queue.\n
        If a port was already in the queue, remove it and add it again.
        '''
        if self.validate_port(port) is not None:
            if port in self.queue:
                await self.remove(port)
            self.queue.append(port)
            
            if len(self.queue) == 1:
                await self.change(port)

    async def remove(self, port):
        '''
        Remove a port from the queue.\n
        If there is another element in the queue, redirect to it.
        '''
        try:
            index = self.queue.index(port)

            if index != 0:
                #   Port in the middle of the queue
                self.queue.remove(port)
            else:
                #   Port at the front of the queue
                self.queue.popleft()
                if len(self.queue) != 0:
                    await self.change(self.queue[0])
                else:
                    await self.change(None)
        finally:
            #   Port not in the queue
            pass
                




#   Testing

if __name__ == '__main__':
    import asyncio as aio

    logging.basicConfig(level=logging.INFO)

    async def main():
        rm = RedirectionManager('192.168.1.2', (25566, 25567), 25565, 2**16)
        
        await rm.append(25566)
        await aio.sleep(2)
        await rm.remove(25566)
        await aio.sleep(2)
        await rm.append(25566)
        await aio.sleep(2)
        await rm.append(25567)
        await aio.sleep(2)
        await rm.remove(25567)
        await aio.sleep(2)
        await rm.remove(25566)
        await aio.sleep(2)
        await rm.append(25568)
        await aio.sleep(2)

    aio.run(main())