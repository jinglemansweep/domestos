from springpython.context import ApplicationContext
from domestos.spring import *

# Tables

class DefaultDBSchema(object):

     def __init__(self, metadata, engine, db_session, logger):

          self.metadata = metadata
          self.engine = engine
          self.db = db_session
          self.logger = logger

          self.device_table = Table("device", self.metadata,
               Column("id", Integer, primary_key=True),
               Column("address", String),
               Column("description", String),
          )

          self.zone_table = Table("zone", self.metadata,
               Column("id", Integer, primary_key=True),
               Column("name", String),
               Column("description", String),
          )

          self.device_zone_table = Table("device_zone", self.metadata,
               Column("device_id", Integer, ForeignKey("device.id"), primary_key=True),
               Column("zone_id", Integer, ForeignKey("zone.id"), primary_key=True),
          )

          mapper(Device, self.device_table)
          mapper(Zone, self.zone_table, properties = {
               "devices": relation(Device, secondary=self.device_zone_table, backref="zones"),
          })
         

     def create_schema(self):
          self.logger.info("Creating initial database schema")
          self.metadata.create_all(self.engine) 
     
     def load_test_data(self):
          self.logger.info("Loading test data")
          lounge_lamp_left = Device("A1", "Lounge Lamp Left")
          lounge_lamp_right = Device("A2", "Lounge Lamp Right")
          kitchen_light = Device("A3", "Kitchen Light")
          zone_lounge = Zone("lounge", "The Lounge")
          zone_lounge.devices = [lounge_lamp_left, lounge_lamp_right,]
          zone_kitchen = Zone("kitchen", "The Kitchen")
          zone_kitchen.devices = [kitchen_light, ]
          self.db.add_all([zone_lounge, zone_kitchen,])
          self.db.commit()
          
          
# Models

class Device(object):
     def __init__(self, address, description):
          self.address = address
          self.description = description

     def __repr__(self):
          return "<Device('%s','%s')>" % (self.address, self.description)

class Zone(object):
     def __init__(self, name, description):
          self.name = name;
          self.description = description
     
     def __repr__(self):
          return "<Zone('%s','%s')>" % (self.name, self.description)
               


    
