import datetime

from domestos.schemas import *


class DefaultDAO(object):
    

    def __init__(self, db, logger):

        self.db = db
        self.logger = logger
                 
        
    def all_states(self):
        
        states = self.db.query(State).all()
        return states
    
        
    def update_state(self, namespace, address, status):
        
        state = self.db.query(State).filter(State.namespace == namespace and State.address == address).first()
        if not state:
            state = State(namespace, address, status, datetime.datetime.utcnow(), datetime.datetime.utcnow())
            self.db.add(state)
        else:
            state.status = status
            state.modify_date = datetime.datetime.utcnow()
        self.db.commit()
        