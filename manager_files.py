'''
Manager file operations.
'''

from shutil import rmtree
from os import path, mkdir, listdir

class ManagerFiles:
    def get_all_templates(self):
        '''
        Return a list of folders inside of templates folder.
        '''
        if path.isdir(self.templates_path):
            return listdir(self.templates_path)
        else:
            self.logging.error('Templates folder did not exist, please fill it with server templates and restart the application.')
            mkdir(self.templates_path)
            return ()

    def create_servers_folder(self):
        '''
        Create a folder for servers.\n
        Delete the previous one if necessary.
        '''
        try:
            if path.exists(self.servers_path):
                rmtree(self.servers_path)
            mkdir(self.servers_path)
        except OSError:
            self.logging.error('Servers folder could not be created.')
    
    def delete_servers_folder(self):
        '''
        Delete servers folder.
        '''
        try:
            rmtree(self.servers_path)
        except OSError:
            self.logging.error('Servers folder could not be deleted.')