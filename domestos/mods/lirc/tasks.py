import socket
import time
from celery.task import task
from base import DTask
from mods.configurator.tasks import get_configuration


@task(base=DTask)
def get_remote_command():
    
    cfg = get_configuration("lirc")
    socket_name = cfg.get("lircd_socket", "/dev/lircd")
    
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.setblocking(True)
    s.connect(socket_name)
    data = str(s.recv(1024))
    parts = data.split("\n")[0].split(" ")

    if len(parts) == 4:
        return dict(raw=parts[0],
                    count=parts[1],
                    command=parts[2],
                    remote=parts[3])
    else:
        return None

