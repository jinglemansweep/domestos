

class BasePlugin(object):

    """ Base Plugin """
    
    def __init__(self, db, logger, payload=None):

        self.db = db        
        self.logger = logger
        self.payload = payload or []
        self.errors = []

        
    def is_valid(self):
        
        errors = []
        for param in self.PARAMETERS:
            if param not in self.payload:
                errors.append("Missing parameter: %s" % (param))
        self.errors = errors
        success = (len(errors) == 0)
        if not success:
            self.logger.warning("Missing plugin payload parameters: %s" % (",".join(errors)))
        return success


class DummyPlugin(BasePlugin):

    """ Dummy Plugin """
    
    NAME = "dummy"
    DESCRIPTION = "Dummy Plugin"
    CAPABILITIES = ["console",]
    PARAMETERS = []
    POLL_INTERVAL = 5


    def execute(self):
        if self.is_valid():
            self.logger.debug("Executing '%s': %s" % (self.NAME, self.payload))
            self.logger.info("DummyPlugin")
            return {"status": "ok"}
        else:
            return {"status": "error"}