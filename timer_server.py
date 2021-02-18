from threading import Thread
import time
import json
import requests
import socket

class SyncedTime:
    def __init__(self):
        self.resync()

    def resync(self):
        webinfo = json.loads(requests.get(
            "http://worldtimeapi.org/api/timezone/Europe/London").content.decode())
        self.startTime = time.time()
        dt = webinfo["datetime"]
        unix = webinfo["unixtime"]

        mili = float("0"+dt[dt.index("."):dt.index("+")])
        self.startTimeUniversal = unix+mili
        self.offset = self.startTimeUniversal - self.startTime

    def time(self):
        return time.time() + self.offset

    def timeSinceResync(self):
        return time.time() - self.startTime


class TimerClientInstance:
    def __init__(self, c, addr):
        self.clientSocket = c
        self.addr = addr
        self.running = False
        self.thread = Thread(target=loop)

    def loop(self):
        while self.running:
            msg = self.clientSocket.recv(1024)
            if msg.decode() == "quit":
                self.running = False

    def send(self, msg):
        self.clientSocket.send(msg.encode())

    def stop(self):
        self.running = False
        self.send("end")
        self.clientSocket.close()


class TimerServer:
    def __init__(self, addr="127.0.0.1", port=25564):
        self.addr = addr
        self.port = port

        self.syncedTime = SyncedTime()
        self.socket = socket.socket()

        self.clients = []
        self.running = False
        self.startTime = self.syncedTime.time()
        self.timerRunning = False

    def start(self):
        if not self.running:
            self.running = True

            self.socket.bind((self.addr, self.port))

            self.ACT = Thread(target=self.acceptConnectionsThread)
            self.ACT.run()

    def acceptConnectionsThread(self):
        while self.running:
            c, addr = self.socket.accept()
            self.clients.append(TimerClientInstance(c, addr))

    def kill(self):
        for i in self.clients:
            i.stop()


if __name__ == "__main__":
    pass
