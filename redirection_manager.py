import logging

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

    async def change(self, new):
        '''
        Changes the current redirector.\n
        If the new port is invalid only stops the previous redirector.
        '''
        if self.current is not None:
            await self.redirectors[self.current].stop()
        
        self.current = None
        if self.redirectors.get(new):
            await self.redirectors[new].start()
            self.current = new

        logging.info(f'Redirection changed to {self.current}')





#   Testing

if __name__ == '__main__':
    import asyncio as aio

    logging.basicConfig(level=logging.INFO)

    async def main():
        rm = RedirectionManager('192.168.1.2', (25566, 25567), 25565, 2**16)
        
        await rm.change(25566)
        await aio.sleep(5)
        await rm.change(None)
        await aio.sleep(5)
        await rm.change(25567)
        await aio.sleep(5)
        await rm.change(25568)
        await aio.sleep(5)

    aio.run(main())