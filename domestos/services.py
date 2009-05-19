import glob
import os
import sys
import time

from domestos.plugins import *
from domestos.schemas import *

class CoreService(object):
  
    """ Core Service """
    
    def __init__(self, amqp_client, cfg, dao, debug, logger, plugins):

        self.amqp_client = amqp_client
        self.cfg = cfg
        self.dao = dao
        self.debug = debug
        self.logger = logger
        self.plugins = plugins
         
        app_name = cfg["app_name"]
        home_folder = os.path.expanduser("~")
        cfg_folder = os.path.join(home_folder, ".%s" % (app_name))
    
        try:
            os.mkdir(cfg_folder)
        except OSError:
            logger.warn("Configuration folder '%s' already exists" % (cfg_folder))     

        self.dao.create_schema() 

        self.logger.info("Service initialised")
        self.logger.debug("Plugins: %s" % (self.plugins))
        

    def run(self):                              
                
        for plugin_inst in self.plugins:
            plugin_inst.amqp_client = self.amqp_client
            plugin_inst.dao = self.dao
            plugin_inst.logger = self.logger
            plugin_inst.initialise()

        self.start_event_loop()

        
    # Message Receiver Functions


    def start_event_loop(self):
        
        while True:    
            for plugin_inst in self.plugins:
                plugin_inst.execute()
                   
    
    

        
