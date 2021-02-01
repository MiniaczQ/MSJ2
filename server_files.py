#	Server file operations

from os import getcwd, makedirs, path, listdir
from shutil import rmtree, copytree

from inside_settings import worlds_file

worlds_file = path.join(getcwd(), worlds_file)

def copy_template(directory):
    pass

def delete_template(directory):
    pass

def create_whitelist(directory, players):
    pass

def delete_whitelist(directory):
    pass

def create_ops(directory, players):
    pass

def delete_ops(directory):
    pass

def delete_world(directory):
    pass

def store_world(directory):
    #   Create directory if needed
    if not path.exists(worlds_file):
        try:
            makedirs(worlds_file)
        except OSError:
            pass
        finally:
            worlds = ()
    else:
        worlds = listdir(worlds_file)

    #   Find last world name for indexing

    copytree(directory, worlds_file)