from domestos.plugins import *
from domestos.models import *

class BasicService(object):

    """
    Service
    """
  
    def __init__(self, logger, db_session, debug):
        """
        Constructor
        """
        self.logger = logger
        self.db = db_session
        self.debug = debug
        self.logger.info("Service initialised")
    
    def get_plugin(self, name):
        plugin = self.get_object(name)
        plugin.logger = self.logger
        return plugin
    
    def run(self):                      
        devs = self.db.query(Device).all()
        print devs