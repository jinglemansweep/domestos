import datetime

class CoreDAO(object):
    
    def __init__(self, logger, schema, session):

        self.logger = logger
        self.schema = schema        
        self.session = session
    
    def create_schema(self):

        self.schema.create_schema()
