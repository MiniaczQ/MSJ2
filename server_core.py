
import server_files

class Server:
    def __init__(self, manager, directory):
        self.directory = directory
        server_files.copy_template(self.directory)

        self.process = None

    def prepare(self):
        server_files.delete_ops(self.directory)
        server_files.create_ops(self.directory)
        server_files.delete_whitelist(self.directory)
        server_files.create_whitelist(self.directory)

    def start(self):
        pass

    def stop(self):
        pass

    def world_reset(self):
        server_files.delete_world(self.directory)

    def world_store(self):
        server_files.store_world(self.directory, )

    def __del__(self):
        server_files.delete_template(self.directory)