import datetime

from domestos.schemas import *


class DefaultDAO(object):
    

    def __init__(self, db, logger):

        self.db = db
        self.logger = logger

        
    def all_devices(self):

        return self.db.query(Device).all()
    
    
    def find_device(self, plugin_name=None, unit_name=None, address=None):
        if not any([plugin_name, unit_name, address,]):
            return
        q = self.db.query(Device)
        if plugin_name:
            q.filter(Device.plugin_name==plugin_name)
        if unit_name:
            q.filter(Device.unit_name==unit_name)
        if address:
            q.filter(Device.address==address)
        return q.first()
    

    def create_trigger(self, device, payload):

        trigger = Trigger(device, payload, None, datetime.datetime.utcnow(), None)
        self.db.add(trigger)
        self.db.commit()