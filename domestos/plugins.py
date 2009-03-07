

class BasePlugin(object):

    """ Base Plugin """
    
    def __init__(self, dao, logger):

        self.dao = dao        
        self.logger = logger


class DummyPlugin(BasePlugin):

    """ Dummy Plugin """

    def execute(self):
        pass


class X10Heyu2Plugin(BasePlugin):

    """ X10 Heyu2 Plugin """
    
    def process_input(self, payload):
        
        self.dao.update_state("x10", payload["address"], payload["command"])