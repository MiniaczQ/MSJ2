#   settings.json parser

from json import load, dump

settings = {}

defaults = {
    'cock': 5,
    'and': False,
    'balls': "bruh"
}

validator = {
    'cock': lambda v: v and type(v) == int,
    'and': lambda v: v and type(v) == bool,
    'balls': lambda v: v and type(v) == str
}

try:
    with open('settings.json', 'r') as __file:
        loaded = load(__file)
        for key in defaults.keys():
            l = loaded.get(key)
            settings[key] = l if validator[key](l) else defaults[key]
except OSError:
    #   No file found
    #   Use defaults
    settings = defaults
finally:
    with open('settings.json', 'w') as __file:
        dump(settings, __file, indent=2)

if __name__ == '__main__':
    print(settings)