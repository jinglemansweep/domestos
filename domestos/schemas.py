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

          self.device_table = Table("device", self.metadata,
               Column("id", Integer, primary_key=True),
               Column("plugin_name", String(length=50)),
               Column("unit_name", String(length=50)),
               Column("address", String(length=255)),
               Column("description", String(length=255)),
               # UniqueConstraint("plugin_name", "unit_name", "address", name="plugin_unit_address")
          )

          self.zone_table = Table("zone", self.metadata,
               Column("id", Integer, primary_key=True),
               Column("name", String(length=50)),
               Column("description", String(length=255)),
          )

          self.device_zone_table = Table("device_zone", self.metadata,
               Column("device_id", Integer, ForeignKey("device.id"), primary_key=True),
               Column("zone_id", Integer, ForeignKey("zone.id"), primary_key=True),
          )

          self.state_table = Table("state", self.metadata,
               Column("id", Integer, primary_key=True),
               Column("device", Integer, ForeignKey("device.id")),
               Column("status", PickleType),
               Column("create_date", DateTime),                                   
               Column("modify_date", DateTime),   
          )          
          
          self.trigger_table = Table("trigger", self.metadata,
               Column("id", Integer, primary_key=True),
               Column("device", Integer, ForeignKey("device.id")),
               Column("payload", PickleType),
               Column("returns", PickleType),
               Column("create_date", DateTime),                                   
               Column("action_date", DateTime),   
          )

          mapper(Device, self.device_table)
          
          mapper(Zone, self.zone_table, properties = {
               "devices": relation(Device, secondary=self.device_zone_table, backref="zones"),
          })

          mapper(State, self.state_table)           
          
          mapper(Trigger, self.trigger_table)          

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

class Device(object):

     """ Device (such as X10) """
     
     def __init__(self, plugin_name, unit_name, address, description):

          self.plugin_name = plugin_name
          self.unit_name = unit_name
          self.address = address
          self.description = description

     def __repr__(self):

          return "<Device('%s','%s','%s')>" % (self.plugin_name, self.unit_name, self.address)


class Zone(object):
     
     """ Zone (such as Kitchen, Lounge, etc.) """

     def __init__(self, name, description):

          self.name = name;
          self.description = description
     
     def __repr__(self):
          
          return "<Zone('%s','%s')>" % (self.name, self.description)
               

     
class State(object):
     
     """ State (current status of devices) """

     def __init__(self, device, status, create_date, modify_date):

          self.device = device
          self.status = status
          self.create_date = create_date
          self.modify_date = modify_date
     
     def __repr__(self):
          
          return "<State('%s','%s')>" % (self.device, self.status)  
     
     
class Trigger(object):
     
     """ Trigger (some kind of input/signal or inbound event) """

     def __init__(self, device, payload, returns, create_date, action_date):

          self.device = device
          self.payload = payload
          self.returns = returns
          self.create_date = create_date
          self.action_date = action_date
     
     def __repr__(self):
          
          return "<Trigger('%s','%s')>" % (self.device, self.payload)   
