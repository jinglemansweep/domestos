#!/usr/bin/env python

import os
import re
import sys
from memcache import Client

args = " ".join(sys.argv[1:])

regex = re.compile("(?P<house>[a-p])(?P<unit>[0-9]?[0-9]\d*?)(?P<command>\w*?)$", re.IGNORECASE)
r = regex.search(args)      
house = str(r.groupdict()["house"]).lower()
unit = str(r.groupdict()["unit"]).lower()
address = "%s%s" % (house, unit)
command = str(r.groupdict()["command"]).lower()

message = {
    "plugin": "x10",
    "payload": {
        "house": house,
	"unit": unit,
	"address": address,
        "command": command,
    },
}

msg_client = Client(["10.0.2.10:21122",])
msg_client.set("domestos.input", message)
