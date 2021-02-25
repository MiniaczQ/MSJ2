'''
Server file operations.
'''

from shutil import rmtree, copytree
from os import mkdir, path, remove

class ServerFiles:
    def copy_template(self):
        '''
        Copy template for the server.\n
        Delete previous server if necessary.
        '''
        try:
            if path.exists(self.directory):
                rmtree(self.directory)
            copytree(self.template_path, self.directory)
        except OSError:
            self.logging.error(f'Template could not be copied for server {self.name}.')

    def delete_template_copy(self):
        '''
        Delete server.
        '''
        if path.exists(self.directory):
            try:
                rmtree(self.directory)
            except OSError:
                self.logging.warning(f'Server {self.name} folder could not be deleted.')

    def delete_whitelist(self):
        '''
        Delete whitelist file.
        '''
        try:
            d = path.join(self.directory, 'whitelist.json')
            if path.isfile(d):
                remove(d)
        except OSError:
            self.logging.warning(f'Server {self.name} whitelist could not be deleted.')

    def delete_ops(self):
        '''
        Delete server operators file.
        '''
        try:
            d = path.join(self.directory, 'ops.json')
            if path.isfile(d):
                remove(d)
        except OSError:
            self.logging.warning(f'Server {self.name} ops could not be deleted.')

    def delete_world(self):
        '''
        Delete world file.
        '''
        try:
            d = path.join(self.directory, 'world')
            if path.exists(d):
                rmtree(d)
        except OSError:
            self.logging.warning(f'Server {self.name} world could not be deleted.')

    def store_world(self, seed):
        '''
        Backup the world.
        '''
        if not path.exists(self.worlds_path):
            try:
                mkdir(self.worlds_path)
            except OSError:
                self.logging.warning(f'Stored worlds folder for server {self.name} could not be created.')
        
        d = path.join(self.worlds_path, seed)
        try:
            copytree(path.join(self.directory, 'world'), d)
            self.logging.info(f'World from server {self.name} with seed {seed} was stored.')
        except OSError:
            self.logging.error(f'World from server {self.name} with seed {seed} could not be stored.')

    def set_properties(self, options):
        '''
        Modify server properties.
        '''
        try:
            settings = {}
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
            self.logging.warning(f'Server {self.name} properties could not be edited.')