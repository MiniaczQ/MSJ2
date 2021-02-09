#   Simplified logging interface

from datetime import datetime
from os import getcwd, path, makedirs
from shutil import rmtree
from sys import stdout
from threading import Lock

from inside_settings import logs_path

class Logger:
    def __init__(self, *streams):
        '''
        Handles logging.\n
        *streams - additional streams to write to
        '''
        self.logs_path = path.join(getcwd(), logs_path)

        #   Create directory if needed
        if not path.exists(self.logs_path):
            try:
                makedirs(self.logs_path)
            except OSError:
                pass

        date_log_path = path.join(self.logs_path, f'{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.txt')
        date_log_file = open(date_log_path, 'w')

        latest_log_path = path.join(self.logs_path, 'latest.txt')
        latest_log_file = open(latest_log_path, 'w')

        self.__streams = streams + (date_log_file, latest_log_file)
        self.lock = Lock()
    
    @staticmethod
    def __finalize(msg):
        '''
        Add time and new line to a message.
        '''
        return f'[{datetime.now().strftime("%H:%M:%S")}] {msg}\n'

    def __write(self, msg):
        '''
        Finalize and send the message to all streams, then flush the streams.
        '''
        with self.lock:
            for stream in self.__streams:
                stream.write(self.__finalize(msg))

            for stream in self.__streams:
                stream.flush()

    def info(self, msg):
        '''
        Send an information level message.
        '''
        self.__write(f'[INFO] {msg}')
    
    def warn(self, msg):
        '''
        Send a warning level message.
        '''
        self.__write(f'[WARN] {msg}')

    def erro(self, msg):
        '''
        Send an error level message.
        '''
        self.__write(f'[ERRO] {msg}')

logger = Logger(stdout)





#   Testing

if __name__ == "__main__":
    from time import sleep

    logger.info('Hello')
    sleep(1)
    logger.warn('world!')
    sleep(1)
    logger.erro(':)')