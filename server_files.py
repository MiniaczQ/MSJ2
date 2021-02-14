#	Server file operations

from datetime import datetime
from shutil import rmtree, copytree
from os import getcwd, makedirs, path, listdir, remove

def copy_template(self):
    try:
        if path.exists(self.directory):
            rmtree(self.directory)
        copytree(self.template_path, self.directory)
    except OSError:
        self.logging.error(f'Template server could not be copied for server {self.name}.')

def delete_template_copy(self):
    try:
        if path.exists(self.directory):
            rmtree(self.directory)
    except OSError:
        self.logging.warning(f'Server {self.name} folder could not be deleted.')

def delete_whitelist(self):
    try:
        d = path.join(self.directory, 'whitelist.json')
        if path.isfile(d):
            remove(d)
    except OSError:
        self.logging.warning(f'Server {self.name} whitelist could not be deleted.')

def delete_ops(self):
    try:
        d = path.join(self.directory, 'ops.json')
        if path.isfile(d):
            remove(d)
    except OSError:
        self.logging.warning(f'Server {self.name} ops could not be deleted.')

def delete_world(self):
    try:
        d = path.join(self.directory, 'world')
        if path.exists(d):
            rmtree(d)
    except OSError:
        self.logging.warning(f'Server {self.name} world could not be deleted.')

def store_world(self, seed):
    if not path.exists(self.worlds_path):
        try:
            makedirs(self.worlds_path)
        except OSError:
            self.logging.warning(f'Stored worlds folder for server {self.name} could not be created.')
    
    d = path.join(self.worlds_path, seed)
    if path.exists(d):
        rmtree(d)
        self.logging.info(f'World from server {self.name} with seed {seed} was stored.')
    copytree(path.join(self.directory, 'world'), d)

def set_properties(self, options):
    settings = {}

    try:
        with open(path.join(self.directory, 'server.properties'), 'r', encoding='utf-8') as file:
            for line in file.readlines():
                if not line.startswith('#'):
                    line = line.strip()
                    equals = line.find('=')
                    settings[line[:equals]] = line[equals+1:]
        
        settings.update(options)
        
        with open(path.join(self.directory, 'server.properties'), 'w', encoding='utf-8') as file:
            for setting in settings.items():
                file.write(f'{setting[0]}={setting[1]}\n')
    except:
        self.logging.warning(f'Server {self.name} could not edit properties.')





#   Testing

if __name__ == '__main__':
    with open('test.txt', 'r') as f:
        pass
    '''
    from time import sleep
    d = path.join(getcwd(), 'server_01')

    copy_template(d)
    store_world(d)
    delete_whitelist(d)
    delete_ops(d)
    delete_world(d)
    delete_template_copy(d)
    '''