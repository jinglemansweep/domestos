import glob
import os
import sys
import time

from domestos.helpers import *
from domestos.plugins import *
from domestos.schemas import *

class BasicService(object):
  
    """ Basic Service """
    
    def __init__(self, cfg, dao, debug, logger, msg_client, plugins):

        self.cfg = cfg
        self.dao = dao
        self.debug = debug
        self.logger = logger
        self.msg_client = msg_client
        self.plugins = plugins

        self.context = {}
        self.plugin_pool = {}     

        self.logger.info("Service initialised")
        self.logger.debug("Plugins: %s" % (self.plugins))
        

    def run(self):                              
                
        self.receive_messages()

        
    # Message Receiver Functions


    def receive_messages(self):
        
        self.logger.debug("Waiting for messages...")
    
        while True:

            msg = self.msg_client.get("domestos.input")
            
            if msg:
                
                self.logger.debug("Msg: %s" % (msg))

                plugin_inst = self.plugins[msg["plugin"]]

                if plugin_inst:
                    plugin_inst.process_input(msg["payload"])
                                
                self.update_contexts()

    
    

    # Context Functions

    def update_contexts(self):

        self.update_calendar_context()


    def update_calendar_context(self):
        
        now = datetime.datetime.now()
        
        self.context["calendar"] = {
             "now": now,
             "year": now.year, 
             "month": now.month, 
             "day": now.day, 
             "hour": now.hour, 
             "minute": now.minute, 
             "second": now.second,
             "dayofweek": now.isoweekday(),
             "weekday": now.isoweekday() in range(1, 5),
             "weekend": now.isoweekday() in range(6, 7),
         }

        