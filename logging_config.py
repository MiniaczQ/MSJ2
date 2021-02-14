'''
Configuration of logging module.
'''

import logging

level = logging.INFO
format = '[%(asctime)s] [%(levelname)s] %(message)s'
datefmt = '%H:%M:%S'

logging.basicConfig(level=level, format=format, datefmt=datefmt)