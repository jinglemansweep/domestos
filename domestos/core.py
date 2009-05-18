import os
import sys

from amqplib import client_0_8 as amqp
from optparse import OptionParser
from springpython.config import Object, XMLConfig
from springpython.context import ApplicationContext, scope
from sqlalchemy import create_engine, Table, Column, DateTime, Integer, String, PickleType, MetaData, ForeignKey, UniqueConstraint
from sqlalchemy.exceptions import IntegrityError
from sqlalchemy.orm import sessionmaker, mapper, relation
from sqlalchemy.databases import mysql 

from domestos.dao import *
from domestos.plugins import *
from domestos.schemas import *
from domestos.services import *

def server_bootstrap():
    
    """ Initial bootstrap process called from command line launcher script """

    parser = OptionParser()

    parser.add_option("-v", "--verbose", action="store_true", dest="debug", default=False, help="Increase output verbosity (debugging)")
    (options, args) = parser.parse_args()
    debug = options.debug
    
    container = ApplicationContext(XMLConfig("domestos/spring/application.xml"))
    service = container.get_object("service")
    service.run()

