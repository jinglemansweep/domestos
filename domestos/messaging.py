from amqplib.client_0_8 import Message

class AMQPClient(object):
    
    def __init__(self, amqp_connection, logger):

        self.amqp_connection = amqp_connection 
        self.amqp_channel = amqp_connection.channel() 
        self.logger = logger

    # Messages

    def get_message(self, queue_name):
        msg = self.amqp_channel.basic_get(queue_name)        
        return msg

    def ack_message(self, msg):
        self.amqp_channel.basic_ack(msg.delivery_tag)
        self.logger.debug("AMQP message (#%i) '%s' acknowleged." % (msg.delivery_tag, msg.body))

    def send_message(self, exchange, routing_key, body):
        msg = Message(body)
        msg.properties["delivery_mode"] = 2
        self.amqp_channel.basic_publish(msg, exchange=exchange, routing_key=routing_key)
        self.logger.debug("AMQP message '%s' sent to '%s' exchange using key '%s'." % (body, exchange, routing_key))

    # Queues, Exchanges and Bindings

    def queue_declare(self, name, durable=False, exclusive=False, auto_delete=False):
        self.amqp_channel.queue_declare(queue=name, durable=durable, exclusive=exclusive, auto_delete=auto_delete)
        self.logger.debug("AMQP queue '%s' declared." % name)

    def exchange_declare(self, name, type="direct", durable=False, auto_delete=False):
        self.amqp_channel.exchange_declare(exchange=name, type=type, durable=durable, auto_delete=auto_delete)
        self.logger.debug("AMQP exchange '%s' declared." % name)

    def queue_bind(self, queue, exchange, routing_key):
        self.amqp_channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)
        self.logger.debug("AMQP key '%s' bound to queue '%s' on exchange '%s'." % (routing_key, queue, exchange))
