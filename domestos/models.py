from sqlalchemy.orm import mapper
from domestos.database import *

class Device(object):
     def __init__(self, address, description):
         self.address = address
         self.description = description

     def __repr__(self):
        return "<Device('%s','%s')>" % (self.address, self.description)

mapper(Device, devices_table)

