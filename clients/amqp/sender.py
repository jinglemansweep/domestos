#!/usr/bin/env python

from amqplib import client_0_8 as amqp
import sys

AMQP_HOST = "192.168.1.70:5672"
AMQP_USERID = "guest"
AMQP_PASSWORD = "guest"
AMQP_VIRTUAL_HOST = "/"

conn = amqp.Connection(host=AMQP_HOST, userid=AMQP_USERID, password=AMQP_PASSWORD, virtual_host=AMQP_VIRTUAL_HOST, insist=False)
chan = conn.channel()

msg = amqp.Message(sys.argv[1])
msg.properties["delivery_mode"] = 2
chan.basic_publish(msg, exchange="exchange", routing_key="x10.input")

chan.close()
conn.close()
