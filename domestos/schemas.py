from springpython.context import ApplicationContext
from domestos.spring import *

# Tables

class DefaultDBSchema(object):

     def __init__(self, metadata, engine, logger):

          self.metadata = metadata
          self.engine = engine
          self.logger = logger

          self.device_table = Table("device", self.metadata,
               Column("id", Integer, primary_key=True),
               Column("address", String),
               Column("description", String),
          )

          self.group_table = Table("group", self.metadata,
               Column("id", Integer, primary_key=True),
               Column("name", String),
               Column("description", String),
          )

          self.device_group_table = Table("device_group", self.metadata,
               Column("device_id", Integer, ForeignKey("device.id"), primary_key=True),
               Column("group_id", Integer, ForeignKey("group.id"), primary_key=True),
          )

          mapper(Device, self.device_table)
          mapper(Group, self.group_table, properties = {
               "devices": relation(Device, secondary=self.device_group_table, backref="groups"),
          })
         

     def create_schema(self):
          self.logger.info("Creating initial database schema")
          self.metadata.create_all(self.engine) 
     
# Models

class Device(object):
     def __init__(self, address, description):
          self.address = address
          self.description = description

     def __repr__(self):
          return "<Device('%s','%s')>" % (self.address, self.description)

class Group(object):
     def __init__(self, name, description):
          self.name = name;
          self.description = description
     
     def __repr__(self):
          return "<Group('%s','%s')>" % (self.name, self.description)
               


    
