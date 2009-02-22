import datetime
import re

from twisted.internet.protocol import Protocol, Factory

from domestos.schemas import *


class TcpEcho(Protocol):

    """ TCP Echo Protocol """
    
    def __init__(self, dao, logger):
        
        self.dao = dao
        self.logger = logger
        self.address = ""
        self.command = ""
        
    def connectionMade(self):

        self.logger.debug("TCP Echo Protocol")

        
    def connectionLost(self, reason):

        self.transport.loseConnection()


    def dataReceived(self, data):
        
        regex = re.compile("(?P<house>[a-p])(?P<unit>[0-9]?[0-9]\d*?)(?P<command>\w*?)$",re.IGNORECASE)
        r = regex.search(data)
        
        house = str(r.groupdict()["house"]).lower()
        unit = str(r.groupdict()["unit"]).lower()
        device_code = "%s%s" % (house, unit)
        command = str(r.groupdict()["command"]).lower()
        output_string = "X10: %s%s %s" % (house, unit, command)
        
        device = self.dao.find_device(plugin_name="x10", address=device_code)
        if device:
            self.dao.create_trigger(device.id, {"command": command})
            self.dao.update_state(device.id, {"state": "on"})
            
        self.logger.debug(output_string)        
        self.transport.write(output_string)

        self.transport.loseConnection()