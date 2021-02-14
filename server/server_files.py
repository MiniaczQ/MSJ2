#	Server file operations

from os import getcwd, makedirs, path, listdir, remove
from shutil import rmtree, copytree
from datetime import datetime

from inside_settings import worlds_path, template_path

worlds_path = path.join(getcwd(), worlds_path)
template_path = path.join(getcwd(), template_path)

def copy_template(directory):
    try:
        if path.exists(directory):
            rmtree(directory)
        copytree(template_path, directory)
    except OSError:
        pass
        #   TODO    Logging

def delete_template_copy(directory):
    try:
        if path.exists(directory):
            rmtree(directory)
    except OSError:
        pass
        #   TODO    Logging

def delete_whitelist(directory):
    try:
        d = path.join(directory, 'whitelist.json')
        if path.isfile(d):
            remove(d)
    except OSError:
        pass
        #   TODO    Logging

def delete_ops(directory):
    try:
        d = path.join(directory, 'ops.json')
        if path.isfile(d):
            remove(d)
    except OSError:
        pass
        #   TODO    Logging

def delete_world(directory):
    try:
        d = path.join(directory, 'world')
        if path.exists(d):
            rmtree(d)
    except OSError:
        pass
        #   TODO    Logging

def store_world(directory, seed):
    if not path.exists(worlds_path):
        try:
            makedirs(worlds_path)
        except OSError:
            pass
    
    d = path.join(worlds_path, seed)
    if path.exists(d):
        rmtree(d)
        #   TODO    Logging
    copytree(path.join(directory, 'world'), d)

def set_properties(directory, options):
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
    from time import sleep
    d = path.join(getcwd(), 'server_01')

    copy_template(d)
    store_world(d)
    delete_whitelist(d)
    delete_ops(d)
    delete_world(d)
    delete_template_copy(d)