#	Server file operations

from datetime import datetime
from shutil import rmtree, copytree
from os import getcwd, makedirs, path, listdir, remove

import hidden_settings
from logging_config import logging

worlds_path = path.join(getcwd(), worlds_path)
template_path = path.join(getcwd(), template_path)

def copy_template(directory):
    try:
        if path.exists(directory):
            rmtree(directory)
        copytree(hidden_settings.template_path, directory)
    except OSError:
        logging.error('Template server not found.')

def delete_template_copy(directory):
    try:
        if path.exists(directory):
            rmtree(directory)
    except OSError:
        logging.warning('Template server copy could not be deleted.')

def delete_whitelist(directory):
    try:
        d = path.join(directory, 'whitelist.json')
        if path.isfile(d):
            remove(d)
    except OSError:
        logging.warning('Server whitelist could not be deleted.')

def delete_ops(directory):
    try:
        d = path.join(directory, 'ops.json')
        if path.isfile(d):
            remove(d)
    except OSError:
        logging.warning('Server ops could not be deleted.')

def delete_world(directory):
    try:
        d = path.join(directory, 'world')
        if path.exists(d):
            rmtree(d)
    except OSError:
        logging.warning('Server world could not be deleted.')

def store_world(directory, seed):
    if not path.exists(worlds_path):
        try:
            makedirs(hidden_settings.worlds_path)
        except OSError:
            logging.warning('Stored worlds folder could not be created.')
    
    d = path.join(worlds_path, seed)
    if path.exists(d):
        rmtree(d)
        logging.info(f'World with seed {seed} was stored.')
    copytree(path.join(directory, 'world'), d)

def set_properties(directory, options):
    settings = {}

    try:
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
    except:
        pass





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