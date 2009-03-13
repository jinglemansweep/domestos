from datetime import datetime

class BasePlugin(object):

    
    """ Base Plugin """

    
    def __repr__(self):
        return str(self.__class__.__name__)
    
    
    def __init__(self, dao, logger):
        self.dao = dao        
        self.logger = logger

        
    def update_values(self):        
        pass


class CalendarPlugin(BasePlugin):
    
    
    """ Calendar Plugin """
    
    
    def initialise(self):
        nodes = self.populate_values()
        self.dao.kv_set_multi(nodes)
        self.logger.info("%s initialised (%i keys set)" % (self, len(nodes)))
    
        
    def update_values(self):
        nodes = self.populate_values()
        self.dao.kv_set_multi(nodes)

        
    def populate_values(self):
        now = datetime.now()
        nodes = {
            "domestos.cal.year": now.year,
            "domestos.cal.month": now.month,
            "domestos.cal.day": now.day,
            "domestos.cal.hour": now.hour,
            "domestos.cal.minute": now.minute,
            "domestos.cal.second": now.second,            
        }
        return nodes
        
    
class X10Heyu2Plugin(BasePlugin):

    
    """ X10 Heyu2 Plugin """

    
    def initialise(self):        
        keys = ["domestos.x10.%s.%s" % (h, u) for u in range(1, 16) for h in ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o",]]
        nodes = dict()
        for key in keys:
            nodes[key] = ""
        self.dao.kv_set_multi(nodes)
        
        self.logger.info("%s initialised (%i keys set)" % (self, len(nodes)))
    

    def update_values(self):
        pass