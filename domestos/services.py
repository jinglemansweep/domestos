import glob
import os
import sys
import time

from domestos.helpers import *
from domestos.plugins import *
from domestos.schemas import *

class BasicService(object):
  
    """ Basic Service """
    
    def __init__(self, cfg, db, debug, factory, logger, protocols, reactor):

        self.cfg = cfg
        self.db = db
        self.debug = debug
        self.factory = factory
        self.logger = logger
        self.protocols = protocols
        self.reactor = reactor

        self.logger.info("Service initialised")
        self.logger.debug("Protocols: %s" % (self.protocols))
        
        
    def run(self):                              
        
        devs = self.db.query(Device).all()
        update_poll = task.LoopingCall(self.update_poll).start(5.0)
        second = task.LoopingCall(self.every_second).start(1.0)
        minute = task.LoopingCall(self.every_minute).start(1.0 * 60)
        hour = task.LoopingCall(self.every_hour).start(1.0 * 60 * 60)
        day = task.LoopingCall(self.every_day).start(1.0 * 60 * 60 * 24)        
        week = task.LoopingCall(self.every_week).start(1.0 * 60 * 60 * 24 * 7) 

        tcp_echo_factory = self.factory()
        tcp_echo_factory.protocol = self.protocols[0]
        self.reactor.listenTCP(int(self.cfg["echo_port"]), tcp_echo_factory)        
        self.reactor.run()


    def update_poll(self):
        
        self.logger.debug("Update Poll")        
        
        get_events_task = task.deferLater(self.reactor, 0, self.get_events)
        get_events_task.addCallback(self.process_get_events)

        get_statuses_task = task.deferLater(self.reactor, 0, self.get_statuses)
        get_statuses_task.addCallback(self.process_get_statuses)
        

    # Reactor Functions


    def get_events(self):
        
        return [{},]    

    
    def get_statuses(self):
        
        return [{},]      
    
        
    # Reactor Callbacks
        

    def process_get_events(self, payload):
        
        self.logger.debug("Process Events: %s" % (payload))

        
    def process_get_statuses(self, payload):
        
        self.logger.debug("Process Statuses: %s" % (payload))        
        

    # Reactor Helper Callbacks
    
        
    def every_second(self):
        
        #self.logger.debug("New Second")       
        pass

    def every_minute(self):

        self.logger.debug("New Minute")  
        

    def every_hour(self):

        self.logger.debug("New Hour")  
        

    def every_day(self):

        self.logger.debug("New Day")
        

    def every_week(self):

        self.logger.debug("New Week")          


    