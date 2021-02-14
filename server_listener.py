'''
Server output interpretation.
'''

import threading
import asyncio as aio
from re import compile, search

import server_reactor
import hidden_settings
from logging_config import logging

_messages = {
    'starting': compile(r'\[..:..:..\] \[Server thread/INFO\]: Starting minecraft server').search,
    'genstart': compile(r'\[..:..:..\] \[Server thread/INFO\]: Preparing start region for dimension minecraft:overworld').search,
    'gendone': compile(r'\[..:..:..\] \[Server thread/INFO\]: Done').search,
    'prompt': compile(r'\[..:..:..\] \[Server thread/INFO\]: <.*?> .*?').search,
    'time0': compile(r'\[..:..:..\] \[Server thread/INFO\]: \[.*?: Set the time to 0\]').search,
    'stop': compile(r'\[..:..:..\] \[Server thread/INFO\]: Stopping server').search,
    'joined': compile(r'\[..:..:..\] \[Server thread/INFO\]: .*? joined the game').search,
    'left': compile(r'\[..:..:..\] \[Server thread/INFO\]: .*? left the game').search,
    'advancement': compile(r'\[..:..:..\] \[Server thread/INFO\]: .*? has made the advancement \[.*?\]').search
}

def _starting(server, line):
    logging.info('Server starting.')

def _genstart(server, line):
    pass
    logging.info('Generation started.')

def _gendone(server, line):
    logging.info('Generation finished.')

def _prompt(server, line):
    logging.info('Prioritized.')

def _time0(server, line):
    logging.info('Speedrunning')

def _stop(server, line):
    logging.info('Server stopped.')

def _joined(server, line):
    player_name = line[33:-16]
    logging.info(f'Player {player_name} joined.')

def _left(server, line):
    player_name = line[33:-14]
    logging.info(f'Player {player_name} left.')

_adv = compile(r'has made the advancement').search
def _advancement(server, line):
    advancement_name = line[_adv(line).end(0)+2:-2]
    logging.info(f'Advancement [{advancement_name}] has been made.')

_reactions = {
    'starting': _starting,
    'genstart': _genstart,
    'gendone': _gendone,
    'prompt': _prompt,
    'time0': _time0,
    'stop': _stop,
    'joined': _joined,
    'left': _left,
    'advancement': _advancement
}

class Server(server_reactor.Server):
    def start_reader(self):
        self.reader.set()
        aio.ensure_future(self.read())

    async def read(self):
        while self.reader.is_set():
            line = await self.process.stdout.readline()
            line = line.decode().strip()
            for name, msg in _messages.items():
                if msg(line):
                    _reactions[name](self, line)
                    break
    
    def stop_reader(self):
        self.reader.clear()