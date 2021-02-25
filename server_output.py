'''
Server output interface.
'''

import asyncio as aio
from re import compile, search

from server_states import States
import aio_loops

class ServerOutput:
    _messages = {
        'starting': compile(r'\[..:..:..\] \[Server thread/INFO\]: Starting minecraft server').search,
        'genstart': compile(r'\[..:..:..\] \[Server thread/INFO\]: Preparing start region for dimension minecraft:overworld').search,
        'gendone': compile(r'\[..:..:..\] \[Server thread/INFO\]: Done').search,
        'prompt': compile(r'\[..:..:..\] \[Server thread/INFO\]: <.*?> .*?').search,
        'time0': compile(r'\[..:..:..\] \[Server thread/INFO\]: \[.*?: Set the time to 0\]').search,
        'stop': compile(r'\[..:..:..\] \[Server thread/INFO\]: Stopping server').search,
        'joined': compile(r'\[..:..:..\] \[Server thread/INFO\]: .*? joined the game').search,
        'left': compile(r'\[..:..:..\] \[Server thread/INFO\]: .*? left the game').search,
        'advancement': compile(r'\[..:..:..\] \[Server thread/INFO\]: .*? has made the advancement \[.*?\]').search,
        'seed': compile(r'idfk').search
    }

    def _starting(self, line):
        '''
        Server is starting.
        '''
        self.change_state(States.Starting)
        self.logging.info(f'Server {self.name} starting.')

    def _genstart(self, line):
        '''
        Generation started.
        '''
        self.server_start_time = self.loop.time()
        self.change_state(States.Generation)
        self.logging.info(f'Server {self.name} generation started.')

    def _gendone(self, line):
        '''
        Generation is done.
        '''
        self.call_redirector(self.manager.redirection_manager.append(self.port))
        delta = self.loop.time() - self.server_start_time
        self.call_manager(self.manager.update_average_startup_time(delta))
        self.call_async(self.write(f'whitelist off'))
        self.call_async(self.write(f'save-off'))
        self.change_state(States.Awaiting)
        self.logging.info(f'Server {self.name} generation finished.')
        self.logging.info(f'Server {self.name} ready in {delta:0.3f} seconds.')

    def _prompt(self, line):
        '''
        Priority prompt detected.
        '''
        self.call_manager(self.manager.prioritize(self))
        self.change_state(States.Prioritized)
        self.logging.info(f'Server {self.name} prioritized.')

    def _time0(self, line):
        '''
        Speedrun start.
        '''
        if self.state == States.Prioritized:
            self.speedrun_start_time = self.loop.time()
            self.manager.server_timer.startTimer()
            self.call_async(self.write(f'whitelist on'))
            self.change_state(States.Speedrunning)
            self.logging.info(f'Server {self.name} speedrun has started.')

    def _stop(self, line):
        '''
        Server is stopping.
        '''
        self.call_manager(self.manager.deprioritize(self))
        self.call_redirector(self.manager.redirection_manager.remove(self.port))
        self.manager.server_killed(self)
        self.change_state(States.Offline)
        self.logging.info(f'Server {self.name} stopped.')
        self.manager.server_timer.resetTimer()

    def _joined(self, line):
        '''
        Player joined.
        '''
        player_name = line[33:-16]
        self.players[player_name] = True
        self.player_count += 1
        if self.player_count == 1:
            self.change_state(States.Probing)
            self.call_async(self.write(f'op {player_name}'))
            self.op = player_name
        self.call_async(self.write(f'whitelist add {player_name}'))
        self.logging.info(f'Player {player_name} joined server {self.name}.')

    def _left(self, line):
        '''
        Player left.
        '''
        player_name = line[33:-14]
        self.players[player_name] = False
        self.player_count -= 1
        if self.player_count == 0 or (self.state == States.Probing and self.op == player_name):
            self.call_async(self.stop())
        self.logging.info(f'Player {player_name} left server {self.name}.')

    _adv = compile(r'has made the advancement').search
    def _advancement(self, line):
        '''
        Advancement achieved.
        '''
        advancement_name = line[ServerOutput._adv(line).end(0)+2:-1]
        if self.advancements.get(advancement_name) is None and self.state == States.Speedrunning:
            self.advancements[advancement_name] = True
            delta = self.loop.time() - self.speedrun_start_time
            self.logging.info(f'Advancement [{advancement_name}] has been made for the first time in [{delta//60:2.0f}:{delta%60:2.3f}].')
    
    def _seed(self, line):
        '''
        here be dragons
        '''
        #   TODO
        self.store_world(line[:])

    _reactions = {
        'starting': _starting,
        'genstart': _genstart,
        'gendone': _gendone,
        'prompt': _prompt,
        'time0': _time0,
        'stop': _stop,
        'joined': _joined,
        'left': _left,
        'advancement': _advancement,
        'seed': _seed
    }

    async def read_loop(self):
        '''
        Server reading loop.
        '''
        while self.reader.is_set():
            line = await self.process.stdout.readline()
            line = line.decode().strip()
            for name, msg in ServerOutput._messages.items():
                if msg(line):
                    ServerOutput._reactions[name](self, line)
                    break
    
    def get_players(self):
        '''
        Returns the list of all players that ever joined the server.
        '''
        return self.players.keys()
    
    def get_online_players(self):
        '''
        Return the list of players who are currently on the server.
        '''
        def skip_offline(players):
            for player, online in players:
                if not online:
                    continue
                yield player
        
        return [skip_offline(self.players.items())]

    def state_changed(self, new_state):
        '''
        Called when server state changes.
        '''
        pass