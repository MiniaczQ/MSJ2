#   settings.json validator

from json import load, dump

from logger import logger

settings = {}

#   Dictionary of default values for every setting
defaults = {
    'server_jar_name': 'server.jar',
    'java_arguments': '',
    'motd': '@name',
    'server_count': 3,
    'local_ports_start': 25566,
    'server_ip': '127.0.0.1',
    'visible_port': 25565,
    'nogui': False
}

#   Unnamed funcitons that return whether a setting is valid
validator = {
    'server_jar_name': lambda v: v is not None and type(v) == str and v.endswith('.jar'),
    'java_arguments': lambda v: v is not None and type(v) == str,
    'motd': lambda v: v is not None and type(v) == str,
    'server_count': lambda v: v is not None and type(v) == int and 0 < v and v <= 26,
    'local_ports_start': lambda v: v is not None and type(v) == int and 0 <= v and v <= 65535,
    'server_ip': lambda v: v is not None and type(v) == str,
    'visible_port': lambda v: v is not None and type(v) == int and 0 <= v and v <= 65535,
    'nogui': lambda v: v is not None and type(v) == bool
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
    settings = defaults
finally:
    with open('settings.json', 'w') as __file:
        dump(settings, __file, indent=2)





#   Testing

if __name__ == '__main__':
    for setting in settings.items():
        print(f'{setting[0]:20} : {setting[1]}')