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
    container = ApplicationContext(CoreApplicationContext())
    service = container.get_object("CoreService")

    
    service.run()
