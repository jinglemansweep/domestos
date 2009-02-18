import os
import sys

from optparse import OptionParser
from springpython.context import ApplicationContext

from domestos.spring import *
from domestos.utils import logsetup

def bootstrap():

    parser = OptionParser()
    #parser.add_option("-f", "--file", dest="filename", help="write report to FILE", metavar="FILE")
    #parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")
    
    parser.add_option("-v", "--verbose", action="store_true", dest="debug", default=False, help="Increase output verbosity (debugging)")
    (options, args) = parser.parse_args()

    debug = options.debug
    
    container = ApplicationContext(CoreApplicationContext(debug=debug))
    logger = container.get_object("Logger")
    service = container.get_object("CoreService")
    cfg = container.get_object("DefaultConfiguration")
    db_schema = container.get_object("DBSchema")
    
    initialise(cfg, logger, db_schema, options)
    
    service.run()
    
def initialise(cfg, logger, db_schema, options):
    # Configuration Folder
    app_name = cfg["app_name"] or "domestos"
    home_folder = os.path.expanduser("~")
    cfg_folder = os.path.join(home_folder, ".%s" % (app_name))
    try:
        os.mkdir(cfg_folder)
    except OSError:
        logger.warn("Configuration folder '%s' already exists" % (cfg_folder))  
    # Database Schema
    db_schema.create_schema()
    db_schema.load_test_data()