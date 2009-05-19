from datetime import datetime
from amqplib.client_0_8 import Message

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
        self.channel.queue_declare(queue="logger", durable=True, exclusive=False, auto_delete=False)
        self.channel.exchange_declare(exchange="exchange", type="direct", durable=True, auto_delete=False,)
        self.channel.queue_bind(queue="logger", exchange="exchange", routing_key="echo")  
        self.channel.queue_bind(queue="logger", exchange="exchange", routing_key="logger")  
        
    def _execute(self):
        msg = self.channel.basic_get("logger")        
        if msg:
            self.channel.basic_ack(msg.delivery_tag)
            self.logger.info("AMQP Logger: %s" % msg.body)


class X10Controller(BasePlugin):
    
    """ AMQP Echo Plugin """

    def __init__(self, amqp_connection, logger):
        self.connection = amqp_connection
        self.channel = self.connection.channel()
        self.logger = logger

    def _start(self):
        self.channel.queue_declare(queue="x10.input", durable=True, exclusive=False, auto_delete=False)
        self.channel.queue_declare(queue="x10.output", durable=True, exclusive=False, auto_delete=False) 
        self.channel.exchange_declare(exchange="exchange", type="direct", durable=True, auto_delete=False,)
        self.channel.queue_bind(queue="x10.input", exchange="exchange", routing_key="x10.input")  
        self.channel.queue_bind(queue="x10.output", exchange="exchange", routing_key="x10.output")  
        
    def _execute(self):
        msg = self.channel.basic_get("x10.input")        
        if msg:
            self.channel.basic_ack(msg.delivery_tag)
            self.logger.info("X10 Input: %s" % msg.body)
            msg = Message("POO")
            msg.properties["delivery_mode"] = 2
            self.channel.basic_publish(msg, exchange="exchange", routing_key="logger")
        

