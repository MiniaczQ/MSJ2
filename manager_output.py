'''
Output interface of the manager.
'''

class ManagerOutput:
    def state_changed(self, new_state):
        '''
        Called when manager state changes.
        '''
        pass

    def server_killed(self, server):
        '''
        Called when server gets killed.
        '''
        self.offline_queue.append(server)
        self.not_empty_queue.set()