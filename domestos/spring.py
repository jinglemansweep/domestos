import os
import sys

from springpython.config import PythonConfig
from springpython.config import Object
from springpython.context import scope
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker, mapper, relation
from sqlalchemy.databases import mysql 
from twisted.internet import reactor
from twisted.internet import task

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
            "db_type": "sqlite",
            "db_username": None,
            "db_password": None,
        }
        return cfg
        
    # Basics
        
    @Object(scope.SINGLETON)
    def Logger(self):
        return logsetup()

    @Object(scope.SINGLETON)
    def Reactor(self):
        return reactor
    
    @Object(scope.SINGLETON)
    def DBMetaData(self):
        return MetaData()
    
    @Object(scope.SINGLETON)
    def DBEngine(self):
        cfg = self.DefaultConfiguration()
        db_filename = os.path.join(os.path.expanduser("~"), ".%s" % (cfg["app_name"]), "%s.db" % (cfg["app_name"]))
        db_conn_str = "%s:///%s" % (cfg["db_type"], db_filename)
        engine = create_engine(db_conn_str, echo=self.debug)
        return engine
        
    @Object(scope.SINGLETON)
    def DBSession(self):
        engine = self.DBEngine()
        session_maker = sessionmaker(bind=engine)
        return session_maker()

    @Object(scope.SINGLETON)
    def DBSchema(self):
        return DefaultDBSchema(db=self.DBSession(), engine=self.DBEngine(), logger=self.Logger(), metadata=self.DBMetaData())
    
    # Services
    
    @Object(scope.SINGLETON)
    def CoreService(self):
        cfg = self.DefaultConfiguration()
        usercode_dir = os.path.join(os.path.expanduser("~"), ".%s" % (cfg["app_name"]), "usercode")
        return BasicService(cfg=self.DefaultConfiguration(), debug=self.debug, db=self.DBSession(), logger=self.Logger(), reactor=self.Reactor())
    
    # Plugins
    
    @Object(scope.PROTOTYPE)
    def DummyPlugin(self):
        return DummyPlugin(db=self.DBSession(), logger=self.Logger())       

