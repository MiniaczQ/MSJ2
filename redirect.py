import threading
import socket

class Forward(threading.Thread):
    '''
    Forwards the connection between user and client.\n
    Don't create instances yourself!
    '''
    def __init__(self, source, destination, redirector):
        threading.Thread.__init__(self)
        self.source = source
        self.destination = destination
        self.redirector = redirector

    def run(self):
        string = ' '
        while string and self.redirector.running:
            string = self.source.recv(1024)
            if string:
                self.destination.sendall(string)
            else:
                self.source.shutdown(socket.SHUT_RD)
                self.destination.shutdown(socket.SHUT_WR)



class Redirector(threading.Thread):
    def __init__(self, port_out, port_in):
        '''
        Redirects connections from one port to another
        port_out - Port you redirect to (the server port)
        port_in - Port you redirect from (default: 25565)
        '''
        threading.Thread.__init__(self)
        self.port_out = port_out
        self.port_in = port_in if port_in else 25565
        self.forwards = []

    def start(self):
        '''
        Starts redirector in a separate thread.
        '''
        self.running = True
        threading.Thread.start(self)
    
    def run(self):
        '''
        Don't call this function!\n
        Use 'start' instead!
        '''
        while self.running:
            try:
                dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                dock_socket.bind(('', self.port_in))
                dock_socket.settimeout(5)
                dock_socket.listen(5)
                while self.running:
                    client_socket = None
                    while self.running:
                        try:
                            client_socket = dock_socket.accept()[0]
                            client_socket.settimeout(5)
                        except socket.timeout:
                            continue
                        break
                    if not self.running:
                        break

                    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_socket.connect(('127.0.0.1', self.port_out))
                    server_socket.settimeout(5)

                    f = Forward(client_socket, server_socket, self)
                    self.forwards.append(f)
                    f.start()

                    f = Forward(server_socket, client_socket, self)
                    self.forwards.append(f)
                    f.start()
            finally:
                pass
    
    def stop(self):
        '''
        Stops the redirector.
        '''
        self.running = False





#   Testing

if __name__ == '__main__':
    r = Redirector(25566, 25565)
    r.start()
    input()
    r.stop()