#!/usr/bin/env python

import os
import re
import subprocess
import sys
import time
from memcache import Client

msg_client = Client(["10.0.2.10:21122",])

while True:

    msg = msg_client.get("domestos.output")

    if msg:
        print msg
    
    else:
        time.sleep(1)