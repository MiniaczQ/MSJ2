'''
Local port redirection class.
'''

import asyncio as aio
import socket

import aio_loops

class Redirector(aio_loops.LoopBase):
    def __init__(self, ip, port_to, port_from, packet_size):
        '''
        Class for local port redirection.\n
        Instantiation has to be done in the same loop as start/stop.\n
        Arguments:\n
        ip          -   Server machine IP (on the network you port forward)\n
        port_to     -   Port to redirect to (port of the server)\n
        port_from   -   Port to redirect from (port the people use)\n
        packet_size -   Bytes per data transfer (preferably power of 2)
        '''
        self.loop = aio_loops.RedirectorLoop
        self.ip = ip
        self.port_to = port_to
        self.port_from = port_from
        self.packet_size = packet_size

        self.server = None

        self.event = aio.Event()

    async def stop(self):
        '''
        Attempts to stop the redirector.\n
        Fails if redirector is not running.
        '''
        if self.server is not None:
            self.server.close()
            await self.server.wait_closed()
            self.server = None

            self.event.clear()
        
    async def start(self):
        '''
        Attempts to start the redirector.\n
        Fails if redirector is already running.
        '''
        if self.server is None:
            self.event.set()

            self.call_async(self.run())

    async def run(self):
        '''
        Start by using 'start' method.\n
        Stop by using 'stop' method.\n
        Ensures lifetime of the server.
        '''
        async def forward(src, dst):
            '''
            Forward data.\n
            Stop if:\n
            - out of data,\n
            - external stop.
            '''
            try:
                data = b' '
                while data and self.event.is_set() and not dst.is_closing() :
                    data = await src.read(self.packet_size)
                    dst.write(data)
                
                if not data or not self.event.is_set():
                    dst.close()
                    await dst.wait_closed()
            except ConnectionAbortedError:
                pass

        async def pair_up(c_reader, c_writer):
            '''
            Received a new client connection.\n
            Pair with a server conenction.\n
            Start forwarding data from:\n
            - client to server,\n
            - server to client.
            '''
            try:
                s_reader, s_writer = await aio.open_connection(self.ip, self.port_to, family=socket.AF_INET)
                self.call_async(forward(s_reader, c_writer))
                self.call_async(forward(c_reader, s_writer))
            except ConnectionRefusedError:
                pass
        
        self.server = await aio.start_server(pair_up, self.ip, self.port_from, family=socket.AF_INET, backlog=5)





#   Testing

if __name__ == '__main__':
    import asyncio as aio

    aio.set_event_loop(aio_loops.RedirectorLoop)

    rm = Redirector('192.168.1.2', 25566, 25565, 2**16)

    rm.call_async(rm.start())
    aio_loops.RedirectorLoop.run_forever()