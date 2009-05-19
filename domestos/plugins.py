import os
import sys
import xmpp
from datetime import datetime


class BasePlugin(object):

    
    """ Base Plugin """

    def __repr__(self):
        return str(self.__class__.__name__)    


class AMQPEcho(BasePlugin):
    
    """ AMQP Echo Plugin """

    def __init__(self):

        self.name = "AMQPEcho"
        self.description = "AMQP Echo Plugin"
        self.author_name = "JingleManSweep"
        self.author_email = "jinglemansweep@gmail.com"

    def initialise(self):

        self.amqp_client.queue_declare(name="logger")
        self.amqp_client.exchange_declare(name="exchange")
        self.amqp_client.queue_bind(queue="logger", exchange="exchange", routing_key="echo")  
        self.amqp_client.queue_bind(queue="logger", exchange="exchange", routing_key="logger") 

        self.logger.info("%s plugin initialised" % self.name)       

    def execute(self):

        msg = self.amqp_client.get_message("logger")       
        if msg:
            self.amqp_client.ack_message(msg)
            self.logger.info("AMQP Logger: %s" % msg.body)


class XMPPController(BasePlugin):

    """ XMPP Controller Plugin """

    def __init__(self, xmpp_hostname, xmpp_port, xmpp_username, xmpp_password):

        self.name = "XMPP Controller"
        self.description = "XMPP Controller Plugin"
        self.author_name = "JingleManSweep"
        self.author_email = "jinglemansweep@gmail.com"

        self.xmpp_hostname = xmpp_hostname
        self.xmpp_port = xmpp_port
        self.xmpp_username = xmpp_username
        self.xmpp_password = xmpp_password

    def initialise(self):

        self.amqp_client.queue_declare(name="xmpp")
        self.amqp_client.exchange_declare(name="exchange")
        self.amqp_client.queue_bind(queue="xmpp", exchange="exchange", routing_key="xmpp")  

        self.jid = xmpp.protocol.JID(self.xmpp_username)
        self.xmpp_client = xmpp.Client(self.jid.getDomain(), debug=[])
        self.xmpp_client.connect((self.xmpp_hostname, int(self.xmpp_port)))
        self.xmpp_client.auth(self.jid.getNode(), self.xmpp_password)
        if not self.xmpp_client.isConnected(): self.xmpp_client.reconnectAndReauth()


        self.logger.info("%s plugin initialised" % self.name)

    def execute(self):

        msg = self.amqp_client.get_message("xmpp")   

        if msg:
            self.amqp_client.ack_message(msg)
            self.logger.info("XMPP Message: %s" % msg.body)
            self.xmpp_client.send(xmpp.Message('jinglemansweep@googlemail.com', msg.body))


class X10Controller(BasePlugin):
    
    """ X10 Controller Plugin """

    def __init__(self, rules=None):

        self.name = "X10 Controller"
        self.description = "X10 Controller Plugin"
        self.author_name = "JingleManSweep"
        self.author_email = "jinglemansweep@gmail.com"

        if not rules: rules = list()

        self.rules = rules

    def initialise(self):

        self.amqp_client.queue_declare(name="x10.input")
        self.amqp_client.queue_declare(name="x10.output")
        self.amqp_client.exchange_declare(name="exchange")
        self.amqp_client.queue_bind(queue="x10.input", exchange="exchange", routing_key="x10.input")  
        self.amqp_client.queue_bind(queue="x10.output", exchange="exchange", routing_key="x10.output") 
        self.logger.info("%s plugin initialised" % self.name)
       
    def execute(self):

        msg = self.amqp_client.get_message("x10.input")   

        if msg:
            msg_body = str(msg.body).split("_")       
            self.logger.info(msg_body)
            self.amqp_client.ack_message(msg)
            x10_source, x10_action = msg_body[0], msg_body[1]
            for rule in self.rules:
                scheduler, event_source, event_action, messages = rule[0], rule[1], rule[2], rule[3]        
                if x10_source == event_source and x10_action == event_action:                
                    
                    self.logger.info("X10 Event: %s %s" % (x10_source, x10_action))
                    for message in messages:
                        self.amqp_client.send_message(exchange="exchange", routing_key=message[0], body=message[1])

