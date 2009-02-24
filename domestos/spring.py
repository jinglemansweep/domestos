import os
import sys

import sched

from springpython.config import PythonConfig
from springpython.config import Object
from springpython.context import scope
from sqlalchemy import create_engine, Table, Column, DateTime, Integer, String, PickleType, MetaData, ForeignKey, UniqueConstraint
from sqlalchemy.exceptions import IntegrityError
from sqlalchemy.orm import sessionmaker, mapper, relation
from sqlalchemy.databases import mysql 
from twisted.internet import reactor
from twisted.internet import task
from twisted.internet.protocol import Protocol, Factory

from domestos.dao import *
from domestos.helpers import *
from domestos.plugins import *
from domestos.protocols import *
from domestos.schemas import *
from domestos.services import *
from domestos.utils import logsetup

class CoreApplicationContext(PythonConfig):

    def __init__(self, debug):
        super(CoreApplicationContext, self).__init__()
        self.debug = debug

    # Configuration
        
    @Object(scope.SINGLETON)
    def DefaultConfiguration(self):
        cfg = {
            "app_name": "domestos",
            "db_type": "mysql",
            "db_host": "127.0.0.1",
            "db_name": "domestos",
            "db_username": "domestos",
            "db_password": "Dom3570$!",
            "echo_port": 8007,
        }
        return cfg
        
    # Basics
        
    @Object(scope.SINGLETON)
    def Logger(self):
        return logsetup()

    @Object(scope.SINGLETON)
    def TwistedReactor(self):
        return reactor

    @Object(scope.SINGLETON)
    def TwistedFactory(self):
        return Factory    
    
    @Object(scope.SINGLETON)
    def TelnetProtocol(self):
        return TelnetProtocol(dao=self.DAO(), logger=self.Logger())
    
    @Object(scope.SINGLETON)
    def DBMetaData(self):
        return MetaData()
    
    @Object(scope.SINGLETON)
    def DBEngine(self):
        cfg = self.DefaultConfiguration()
        db_filename = os.path.join(os.path.expanduser("~"), ".%s" % (cfg["app_name"]), "%s.db" % (cfg["app_name"]))
        db_conn_str = "%s://%s:%s@%s/%s?charset=utf8&use_unicode=0" % (cfg["db_type"], cfg["db_username"], cfg["db_password"], cfg["db_host"], cfg["db_name"])
        engine = create_engine(db_conn_str, echo=self.debug)
        return engine
        
    @Object(scope.SINGLETON)
    def DBSession(self):
        engine = self.DBEngine()
        session_maker = sessionmaker(bind=engine)
        return session_maker()

    @Object(scope.SINGLETON)
    def DAO(self):
        return DefaultDAO(db=self.DBSession(), logger=self.Logger())
    
    @Object(scope.SINGLETON)
    def DBSchema(self):
        return DefaultDBSchema(db=self.DBSession(), 
                               engine=self.DBEngine(), 
                               logger=self.Logger(), 
                               metadata=self.DBMetaData())
    
    @Object(scope.PROTOTYPE)
    def DefaultScheduler(self):
        current_time_function = time.time
        delay_by_one_unit_function = time.sleep
        scheduler = sched.scheduler(current_time_function, delay_by_one_unit_function)        
        return scheduler
    
    # Services
    
    @Object(scope.SINGLETON)
    def CoreService(self):
        protocols = {"tcp_echo": self.TelnetProtocol}
        plugins = {"dummy": self.DummyPlugin()}
        return BasicService(cfg=self.DefaultConfiguration(), 
                            debug=self.debug, 
                            dao=self.DAO(), 
                            factory=self.TwistedFactory(),
                            logger=self.Logger(),
                            plugins = plugins,
                            protocols=protocols,
                            reactor=self.TwistedReactor(),
                            scheduler=self.DefaultScheduler())
    
    # Plugins
    
    @Object(scope.PROTOTYPE)
    def DummyPlugin(self):
        return DummyPlugin(db=self.DBSession(), 
                           logger=self.Logger())       

