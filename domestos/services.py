import glob
import os
import sys
import time

from domestos.helpers import *
from domestos.plugins import *
from domestos.schemas import *

class BasicService(object):
  
    """ Basic Service """
    
    def __init__(self, cfg, dao, debug, logger, memcache_client, plugins, scheduler):

        self.cfg = cfg
        self.dao = dao
        self.debug = debug
        self.logger = logger
        self.memcache_client = memcache_client
        self.plugins = plugins
        self.scheduler = scheduler

        self.context = {}
        self.plugin_pool = {}     

        self.logger.info("Service initialised")
        self.logger.debug("Plugins: %s" % (self.plugins))
        

    def run(self):                              
                
        for plugin_inst in self.plugins:
            plugin_inst.initialise()
        
        self.scheduler.start()
        self.start_event_loop()

        
    # Message Receiver Functions


    def start_event_loop(self):
        
        while True:    
            for plugin_inst in self.plugins:
                plugin_inst.update_values()
                   
    
    

        