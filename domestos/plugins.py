from datetime import datetime

class BasePlugin(object):

    
    """ Base Plugin """

    def __repr__(self):
        return str(self.__class__.__name__)    

class AMQPEcho(BasePlugin):
    
    """ AMQP Echo Plugin """

    def __init__(self, amqp_connection, logger):
        self.connection = amqp_connection
        self.channel = self.connection.channel()
        self.logger = logger

    def _start(self):
        self.channel.queue_declare(queue="queue_core", durable=True, exclusive=False, auto_delete=False)
        self.channel.exchange_declare(exchange="exchange_core", type="direct", durable=True, auto_delete=False,)
        self.channel.queue_bind(queue="queue_core", exchange="exchange_core", routing_key="core")  
        
    def _execute(self):
        msg = self.channel.basic_get("queue_core")        
        if msg:
            self.channel.basic_ack(msg.delivery_tag)
            self.logger.info("AMQPEcho: %s" % (msg.body))
        

