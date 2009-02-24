import glob
import os
import sched
import sys
import threading
import time

from domestos.helpers import *
from domestos.plugins import *
from domestos.schemas import *

class BasicService(object):
  
    """ Basic Service """
    
    def __init__(self, cfg, dao, debug, factory, logger, plugins, protocols, reactor, scheduler):

        self.cfg = cfg
        self.dao = dao
        self.debug = debug
        self.factory = factory
        self.logger = logger
        self.plugins = plugins
        self.protocols = protocols
        self.reactor = reactor
        self.scheduler = scheduler

        self.plugin_pool = {}
        self.protocol_pool = {}        
        
        self.logger.info("Service initialised")
        self.logger.debug("Protocols: %s" % (self.protocols))
        self.logger.debug("Plugins: %s" % (self.plugins))
        

    def run(self):                              
                
        self.register_protocols()
        t = threading.Thread(target=self.run_scheduler).start()            
        self.reactor.run()


    def register_protocols(self):
        
        for p in self.protocols:
            protocol = self.protocols[p]
            self.protocol_pool[p] = self.factory()
            self.protocol_pool[p].protocol = protocol
            self.reactor.listenTCP(int(protocol().PORT), self.protocol_pool[p])
        
        
        
    # Scheduler Functions


    def event_poller(self):
        
        self.logger.debug("Adding events")

        states = self.dao.all_states()
        self.logger.debug("States: %s" % (states))
        
        self.scheduler.enter(1, 1, self.event_poller, ())
        pass
    
    
    def run_scheduler(self):
        
        self.logger.debug("Starting scheduler")
        self.scheduler.enter(1, 1, self.event_poller, ())
        self.scheduler.run()
        


    