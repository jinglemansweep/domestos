from springpython.config import PythonConfig
from springpython.config import Object
from springpython.context import scope
from sqlalchemy.orm import sessionmaker

from domestos.models import *
from domestos.plugins import *
from domestos.services import *
from domestos.utils import logsetup

class CoreApplicationContext(PythonConfig):

    def __init__(self):
        super(CoreApplicationContext, self).__init__()

    @Object(scope.SINGLETON)
    def CoreService(self):
        return BasicService(logger=self.Logger(), db_session=self.DBSession(), debug=False)

    @Object(scope.SINGLETON)
    def Logger(self):
        return logsetup()

    @Object(scope.SINGLETON)
    def DBSession(self):
        engine.echo = False
        session_maker = sessionmaker(bind=engine)
        return session_maker()
    
    @Object(scope.PROTOTYPE)
    def DummyPlugin(self):
        return DummyPlugin(logger=self.Logger(), db_session=self.DBSession())       
            
    def NotExposed(self):
        pass
