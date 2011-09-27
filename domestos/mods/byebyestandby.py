from celery.task import task
from base import DTask
from socket import socket, AF_INET, SOCK_DGRAM

@task(base=DTask)
def switch_device(code, state):
    raw_state = 1 if state else 0
    h, u = code[0], code[1:]
    cmd = "D:%i%s%02d:E" % (int(raw_state), h.upper(), int(u))
    s = socket(AF_INET, SOCK_DGRAM)
    s.sendto(cmd, host, port)
    
