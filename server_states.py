'''
Possible states the server can be in.
'''

class States:
    Offline = 0
    Starting = 1
    Generation = 2
    Awaiting = 3
    Probing = 4
    Prioritized = 5
    Speedrunning = 6
    Stopping = 7

States.inverse = dict((value, key) for key, value in States.__dict__.items() if not key.startswith('__') and not callable(key))