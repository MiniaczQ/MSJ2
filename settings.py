'''
Loading and validation of settings.
'''

from json import load, dump

from logging_config import logging

settings = {}

#   Dictionary of default values for every setting
defaults = {
    'server_jar_name': 'server.jar',
    'java_arguments': '',
    'motd': '%(name)s',
    'server_count': 3,
    'local_ports_start': 26000,
    'server_ip': '192.168.2.129',
    'visible_port': 25565,
    'nogui': False,
    'default_template': '1.14.4'
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
    'nogui': lambda v: v is not None and type(v) == bool,
    'default_template': lambda v: v is not None and type(v) == str
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
                logging.warning(f'Invalid setting "{key}" with value: {l}')
except OSError:
    settings = defaults
finally:
    with open('settings.json', 'w') as __file:
        dump(settings, __file, indent=2)





#   Testing

if __name__ == '__main__':
    for setting in settings.items():
        print(f'{setting[0]:20} : {setting[1]}')