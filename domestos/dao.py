import datetime

from domestos.schemas import *


class DefaultDAO(object):
    

    def __init__(self, db, logger, memcache_client):

        self.db = db
        self.logger = logger
        self.memcache_client = memcache_client
                 
        
    def kv_set(self, key, value):
        
        key = str(key)
        self.memcache_client.set(key, value)


    def kv_set_multi(self, dictionary=None):
        
        if not dictionary: dictionary = dict()
        self.memcache_client.set_multi(dictionary)        
        
            
    def kv_get(self, key):
        
        value = self.memcache_client.get(str(key))
        return value

    def kv_get_multi(self, keys=None):
        
        if not keys: keys = list()
        values = self.memcache_client.get_multi(keys)
        return values  
    