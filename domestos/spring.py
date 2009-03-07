import os
import sys
import sched

from memcache import Client
from springpython.config import PythonConfig
from springpython.config import Object
from springpython.context import scope
from sqlalchemy import create_engine, Table, Column, DateTime, Integer, String, PickleType, MetaData, ForeignKey, UniqueConstraint
from sqlalchemy.exceptions import IntegrityError
from sqlalchemy.orm import sessionmaker, mapper, relation
from sqlalchemy.databases import mysql 

from domestos.dao import *
from domestos.helpers import *
from domestos.plugins import *
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
            "msg_servers": ["10.0.2.10:21122",],
        }
        return cfg
        
    # Basics
        
    @Object(scope.SINGLETON)
    def Logger(self):
        return logsetup()

    @Object(scope.SINGLETON)
    def MsgClient(self):
        cfg = self.DefaultConfiguration()
        return Client(cfg["msg_servers"])
    
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
        
    # Services
    
    @Object(scope.SINGLETON)
    def CoreService(self):

        plugins = {"x10": self.X10Heyu2Plugin()}
        return BasicService(cfg=self.DefaultConfiguration(), 
                            debug=self.debug, 
                            dao=self.DAO(), 
                            logger=self.Logger(),
                            msg_client=self.MsgClient(),
                            plugins = plugins,)
    
    # Plugins
    
    @Object(scope.PROTOTYPE)
    def DummyPlugin(self):
        return DummyPlugin(dao=self.DAO(), 
                           logger=self.Logger())       

    @Object(scope.PROTOTYPE)
    def X10Heyu2Plugin(self):
        return X10Heyu2Plugin(dao=self.DAO(), 
                           logger=self.Logger())  
