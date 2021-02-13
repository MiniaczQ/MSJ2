import asyncio as aio
import threading
import socket

class Redirector:
    def __init__(self, ip, port_to, port_from = 25565, packet_size = 8192):
        '''
        Class for local port redirection.\n
        Use 'create_redirector' for creation in external loops.\n
        Arguments:\n
        ip          -   Server machine IP (on the network you port forward)\n
        port_to     -   Port to redirect to (port of the server)\n
        port_from   -   Port to redirect from (port the people use)\n
        packet_size -   Bytes per data transfer (preferably power of 2)
        '''
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
        Attempts to start the redirector.
        Fails if redirector is already running.
        '''
        if self.server is None:
            self.event.set()

            aio.ensure_future(self.run())

    async def run(self):
        '''
        Start by using 'start' method.\n
        Stop by using 'stop' method.\n
        Ensures lifetime of the server.
        '''
        async def forward(src, dst):
            '''
            Forward data.\n
            Stop if:
            - out of data,
            - external stop.
            '''
            data = b''
            while data and not dst.is_closing():
                data = await src.read(self.packet_size)
                dst.write(data)

                if not self.event.is_set():
                    dst.close()
                    await dst.wait_closed()
                    break

        async def pair_up(c_reader, c_writer):
            '''
            Received a new client connection.\n
            Pair with a server conenction.\n
            Start forwarding data from:\n
            - client to server,\n
            - server to client.
            '''
            s_reader, s_writer = await aio.open_connection(self.ip, self.port_to, family=socket.AF_INET)
            f1 = aio.ensure_future(forward(s_reader, c_writer))
            f2 = aio.ensure_future(forward(c_reader, s_writer))
        
        self.server = await aio.start_server(pair_up, self.ip, self.port_from, family=socket.AF_INET, backlog=5)
        await self.event.wait()

async def create_redirector(*args, **kwargs):
    '''
    Wrap of Redirector initialization.\n
    Use to create the instance in a remote loop.
    '''
    return Redirector(*args, **kwargs)





#   Testing

if __name__ == '__main__':
    async def main():
        r = await create_redirector('192.168.1.2', 26000, 26003, 2**16)
        await start_stop(r)

    async def start_stop(r):
        aio.ensure_future(r.start())
        await aio.sleep(10)
        aio.ensure_future(r.stop())

    aio.run(main())