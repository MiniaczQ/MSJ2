#	Server file operations

from os import getcwd, makedirs, path, listdir, remove
from shutil import rmtree, copytree
from datetime import datetime

from inside_settings import worlds_path, template_path
from logger import logger

worlds_path = path.join(getcwd(), worlds_path)
template_path = path.join(getcwd(), template_path)

class ServerFolderError(Exception):
    pass

def copy_template(directory):
    try:
        copytree(template_path, directory)
    except OSError:
        logger.erro('Failed to copy the server template.')
        raise ServerFolderError('Failed to copy the server template.')

def delete_template_copy(directory):
    try:
        rmtree(directory)
    except OSError:
        logger.erro('Failed to delete a server.')
        raise ServerFolderError('Failed to delete a server.')

def delete_whitelist(directory):
    try:
        remove(path.join(directory, 'whitelist.json'))
    except OSError:
        logger.warn('Failed to delete "whitelist.json".')

def delete_ops(directory):
    try:
        print(path.join(directory, 'ops.json'))
        remove(path.join(directory, 'ops.json'))
    except OSError:
        logger.warn('Failed to delete "ops.json".')

def delete_world(directory):
    try:
        rmtree(path.join(directory, 'world'))
    except OSError:
        logger.warn('Failed to delete the world folder.')

def store_world(directory):
    if not path.exists(worlds_path):
        try:
            makedirs(worlds_path)
        except OSError:
            pass

    copytree(path.join(directory, 'world'), path.join(worlds_path, f'world-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'))





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