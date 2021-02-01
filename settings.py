#   settings.json validator

from json import load, dump

from logger import logger

settings = {}

defaults = {
    'cock': 5,
    'and': False,
    'balls': "bruh"
}

validator = {
    'cock': lambda v: v is not None and type(v) == int,
    'and': lambda v: v is not None and type(v) == bool,
    'balls': lambda v: v is not None and type(v) == str
}

try:
    with open('settings.json', 'r') as __file:
        loaded = load(__file)
        for key in defaults.keys():
            l = loaded.get(key)
            if validator[key](l):
                settings[key] = l
            else:
                settings[key] = defaults[key]
                logger.warn(f'Invalid setting "{key}" with value: {l}')
except OSError:
    #   No file found
    #   Use defaults
    settings = defaults
finally:
    with open('settings.json', 'w') as __file:
        dump(settings, __file, indent=2)

if __name__ == '__main__':
    print(settings)