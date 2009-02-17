from domestos.models import *

class DefaultDAO(object):
    
    def __init__(self, db_session, logger):
        self.logger = logger
        self.db = db_session
        
    def all_devices(self):
        return self.db.query(Device).all()
    