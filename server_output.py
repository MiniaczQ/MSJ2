'''
Server output interface.
'''

import asyncio as aio
from re import compile, search

from server_states import States

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

def _starting(self, line):
    self.change_state(States.Starting)
    self.logging.info(f'Server {self.name} starting.')

def _genstart(self, line):
    self.change_state(States.Generation)
    self.logging.info(f'Server {self.name} generation started.')

def _gendone(self, line):
    delta = aio.get_event_loop().time() - self.server_start_time
    #   TODO    Update average start time
    self.change_state(States.Awaiting)
    self.logging.info(f'Server {self.name} generation finished.')
    self.logging.info(f'Server {self.name} ready in {delta:0.3f} seconds.')

def _prompt(self, line):
    self.change_state(States.Prioritized)
    self.logging.info(f'Server {self.name} prioritized.')

def _time0(self, line):
    self.speedrun_start_time = aio.get_event_loop().time()
    self.change_state(States.Speedrunning)
    self.logging.info(f'Server {self.name} speedrun has started.')

def _stop(self, line):
    self.change_state(States.Offline)
    self.logging.info(f'Server {self.name} stopped.')

def _joined(self, line):
    player_name = line[33:-16]
    if len(self.players.items()) == 0:
        self.change_state(States.Probing)
        self.write(f'op {player_name}')
    self.players[player_name] = True
    self.logging.info(f'Player {player_name} joined server {self.name}.')

def _left(self, line):
    player_name = line[33:-14]
    self.players[player_name] = False
    self.logging.info(f'Player {player_name} left server {self.name}.')

_adv = compile(r'has made the advancement').search
def _advancement(self, line):
    advancement_name = line[_adv(line).end(0)+2:-1]
    if self.advancements.get(advancement_name) is None:
        self.advancements[advancement_name] = True
        delta = aio.get_event_loop().time() - self.speedrun_start_time
        self.logging.info(f'Advancement [{advancement_name}] has been made for the first time in [{delta//60}:{delta%60:0.3f}].')

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

class ServerOutput:
    async def read_loop(self):
        '''
        Server reading loop.
        '''
        while self.reader.is_set():
            line = await self.process.stdout.readline()
            line = line.decode().strip()
            for name, msg in _messages.items():
                if msg(line):
                    _reactions[name](self, line)
                    break
    
    def get_players(self):
        '''
        Returns the list of all players that ever joined the server.
        '''
        return self.players.keys()

    def state_changed(self, new_state):
        '''
        Called when server state changes.
        '''
        pass