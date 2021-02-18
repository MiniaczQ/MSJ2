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
    def __init__(self, parent, c, addr):
        self.parent = parent
        self.clientSocket = c
        self.addr = addr
        self.running = True
        self.thread = Thread(target=self.loop)
        self.thread.start()

    def loop(self):
        try:
            while self.running:
                msg = self.clientSocket.recv(1024)
                if msg.decode() == "quit":
                    self.running = False
                    self.send("end")
        except:
            pass
        self.parent.removeClient(self)
        

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
        self.pauseTime = 0
        self.timerStatus = "stopped"

    def start(self):
        if not self.running:
            self.running = True

            self.socket.bind((self.addr, self.port))
            self.socket.listen(50)

            self.acceptConnectionsThread = Thread(target=self.acceptConnectionsLoop)
            self.acceptConnectionsThread.start()
    
    def startTimer(self):
        if self.timerStatus != "running":
            self.startTime = self.syncedTime.time() - self.pauseTime
            self.timerStatus = "running"
        self.updateClients()
    
    def resetTimer(self):
        if self.timerStatus != "stopped":
            self.pauseTime = 0
            self.timerStatus = "stopped"
        self.updateClients()
    
    def pauseTimer(self):
        if self.timerStatus == "running":
            self.pauseTime = self.syncedTime.time()-self.startTime
            self.timerStatus = "paused"
        self.updateClients()
    
    def updateClient(self,client):
        if self.timerStatus == "stopped":
            client.send("stop")
        elif self.timerStatus == "running":
            client.send("running:"+str(self.startTime))
        elif self.timerStatus == "paused":
            client.send("paused:"+str(self.pauseTime))
    
    def updateClients(self):
        for client in self.clients:
            self.updateClient(client)
    
    def sendToAll(self,msg):
        for client in self.clients:
            client.send(msg)

    def acceptConnectionsLoop(self):
        while self.running:
            try:
                c, addr = self.socket.accept()
                client = TimerClientInstance(self, c, addr)
                if self.running:
                    self.clients.append(client)
                    print("[Timer Server] Client '"+str(addr)+"' connected.")
                    self.updateClient(client)
            except:
                pass
    
    def setTime(self, x):
        self.pauseTime = x
        self.startTime = self.syncedTime.time()-x

    def getTime(self):
        if self.timerStatus == "stopped":
            return 0.0
        elif self.timerStatus == "running":
            return self.syncedTime.time()-self.startTime()
        elif self.timerStatus == "paused":
            return self.pauseTime

    def kill(self):
        for i in self.clients:
            i.stop()
        self.running = False
        self.socket.close()
        
    
    def removeClient(self, client):
        self.clients.remove(client)


if __name__ == "__main__":
    import keyboard
    ts = TimerServer()
    ts.start()
    keyboard.add_hotkey("alt+\\",ts.resetTimer)
    keyboard.add_hotkey("alt+[",ts.startTimer)
    keyboard.add_hotkey("alt+]",ts.pauseTimer)
    input()
    ts.kill()