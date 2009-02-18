import glob
import os
import sys
import time
from domestos.helpers import *
from domestos.plugins import *
from domestos.schemas import *

class BasicService(object):

    """
    Service
    """
  
    def __init__(self, logger, db_session, usercode_dir, debug):
        """
        Constructor
        """
        self.logger = logger
        self.db = db_session
        self.usercode_dir = usercode_dir
        self.usercode = {}
        self.debug = debug
        self.dt = DT()
        self.logger.info("Service initialised")
    
    def run(self):                      
        devs = self.db.query(Device).all()
        sys.path.append(self.usercode_dir)                                   
        if os.path.exists(os.path.join(self.usercode_dir, "startup.py")):
            self.usercode["startup"] = __import__("startup")        
        if os.path.exists(os.path.join(self.usercode_dir, "loop.py")):
            self.usercode["loop"] = __import__("loop")

        if "startup" in self.usercode:
            self.usercode["startup"].run(self)
        while True:
            self.dt.update()
            time.sleep(0.1)
            if "loop" in self.usercode:
                self.usercode["loop"].run(self)