

class BasePlugin(object):

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
            logger.warning("Missing plugin payload parameters: %s" % (",".join(errors)))
        return success


class DummyPlugin(BasePlugin):
    """
    Dummy Plugin
    """
    
    NAME = "dummy"
    DESCRIPTION = "Dummy Plugin"
    CAPABILITIES = ["console",]
    PARAMETERS = ["name", "age", "message",]

    #def __repr__(self):
    #    return self.NAME

    def execute(self):
        if self.is_valid():
            logger.debug("Executing '%s': %s" % (self.NAME, self.payload))
            logger.info("DummyPlugin")