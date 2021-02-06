#   Edits specific server properties

from os import path

def edit(directory, options):
    settings = {}

    with open(path.join(directory, 'server.properties'), 'r', encoding='utf-8') as file:
        for line in file.readlines():
            if not line.startswith('#'):
                line = line.strip()
                equals = line.find('=')
                settings[line[:equals]] = line[equals+1:]
    
    settings.update(options)
    
    with open(path.join(directory, 'server.properties'), 'w', encoding='utf-8') as file:
        for setting in settings.items():
            file.write(f'{setting[0]}={setting[1]}\n')





#   Testing

if __name__ == '__main__':
    options = {
        'server-port': 25565
    }
    edit('template', options)