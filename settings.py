#   settings.json parser

from json import load, dump

__defaults = {
    'log_path': 'logs'
}

try:
    with open('settings.json', 'r') as __file:
        __settings = load(__file)
        __fix_settings = False

        __g = globals()

        for key, value in __defaults.items():
            if not (__settings.get(key) and type(__settings[key]) == type(__defaults[key])):
                __settings[key] = __defaults[key]
                __fix_settings = True
            __g[key] = __settings[key]
        
    if __fix_settings:
        with open('settings.json', 'w') as __file:
            dump(__settings, __file, indent=2)

except OSError:
    #   File not found, use default settings, create a settings file

    with open('settings.json', 'w') as __file:
        dump(__defaults, __file, indent=2)
    pass





#   Testing

if __name__ == '__main__':
    print(__settings)


setting = (default, validator)

def validate(dictionary, validator):
    for key, value in dictionary.update(defaults).items():
        