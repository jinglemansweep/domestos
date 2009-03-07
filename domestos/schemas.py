from springpython.context import ApplicationContext

from domestos.spring import *

# Tables

class DefaultDBSchema(object):

     """ Default database schema - table configurations and mappings """
     
     def __init__(self, db, engine, logger, metadata):

          self.db = db
          self.engine = engine
          self.logger = logger
          self.metadata = metadata

          self.state_table = Table("state", self.metadata,
               Column("id", Integer, primary_key=True),
               Column("namespace", String(length=255)),
               Column("address", String(length=255)),
               Column("status", String(length=255)),
               Column("create_date", DateTime),                                   
               Column("modify_date", DateTime),   
          )          

          mapper(State, self.state_table)           
    

     def create_schema(self):
          
          self.logger.info("Creating initial database schema")
          self.metadata.create_all(self.engine) 
     
          
     def load_test_data(self):
          
          self.logger.info("Loading test data")
          lounge_lamp_left = Device("x10", "lamp", "a1", "Lounge Lamp Left")
          lounge_lamp_right = Device("x10", "lamp", "a2", "Lounge Lamp Right")
          kitchen_light = Device("x10", "light", "a3", "Kitchen Light")
          test_device = Device("x10", "dummy", "a7", "Test Device")
          zone_lounge = Zone("lounge", "The Lounge")
          zone_lounge.devices = [lounge_lamp_left, lounge_lamp_right,]
          zone_kitchen = Zone("kitchen", "The Kitchen")
          zone_kitchen.devices = [kitchen_light, test_device, ]
          self.db.add_all([zone_lounge, zone_kitchen,])
          try:
               self.db.commit()
          except IntegrityError:
               self.db.rollback()
          
          
# Models
     
class State(object):
     
     """ State """

     def __init__(self, namespace, address, status, create_date, modify_date):

          self.namespace = namespace
          self.address = address
          self.status = status
          self.create_date = create_date
          self.modify_date = modify_date
     
     def __repr__(self):
          
          return "<State('%s','%s')>" % (self.namespace, self.address)  
     
     
