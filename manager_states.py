'''
States of the manager.
'''

class States:
    Stopped = 0
    Cycling = 1
    Priority = 2

    @staticmethod
    def validate(state):
        return state in States.inverse.keys()

States.inverse = dict((value, key) for key, value in States.__dict__.items() if not key.startswith('__') and not callable(key))