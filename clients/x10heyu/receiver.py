#!/usr/bin/env python

import os
import re
import subprocess
import sys
import time
from memcache import Client

# Configuration

MSG_HOSTS = ["127.0.0.1:21122",]
HEYU2_PATH = "/usr/local/bin/heyu2"

# Main Loop

msg_client = Client(MSG_HOSTS)

while True:

    msg = msg_client.get("domestos.output")

    if msg:
        plugin = msg["plugin"]
        payload = msg["payload"]
        house, unit, command = payload["house"], payload["unit"], payload["command"]
        if all([house, unit, command]):
                heyu_opts = "%s %s%s" % (command, house, unit)
                print heyu_opts
                subprocess.Popen("%s %s"  % (HEYU2_PATH, heyu_opts), shell=True)
    
    else:
        time.sleep(1)
