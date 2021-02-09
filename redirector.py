import asyncio as aio
import threading
import socket

class Redirector:
    def __init__(self, port_in, ip = '127.0.0.1', port_out = 25565, packet_size = 8192):
        self.event = threading.Event()
        self.server = None
        self.ip = ip
        self.port_in = port_in
        self.port_out = port_out
        self.packet_size = packet_size

    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.event.set()
            self.server = None
        
    async def start(self):
        if not self.server:
            async def forward(src, dst):
                data = await src.read(self.packet_size)
                while data:
                    dst.write(data)
                    if self.event.is_set():
                        dst.close()
                        await dst.wait_closed()
                        return
                    data = await src.read(self.packet_size)

            async def pair_up(c_reader, c_writer):
                s_reader, s_writer = await aio.open_connection(self.ip, self.port_out, family=socket.AF_INET)
                f1 = aio.ensure_future(forward(s_reader, c_writer))
                f2 = aio.ensure_future(forward(c_reader, s_writer))
            
            self.event.clear()
            self.server = await aio.start_server(pair_up, self.ip, self.port_in, family=socket.AF_INET, backlog=5)





#   Testing

if __name__ == '__main__':
    async def main(r):
        await r.start()
        await aio.sleep(10)
        await r.stop()
        await aio.sleep(5)

    redirector = Redirector(25566)
    aio.run(main(redirector))