import time
from celery.task import task
from base import DTask
from utils import get_module_config

@task(base=DTask)
def get_remote_command():
    cfg = get_module_config()
    print cfg
    time.sleep(5) # Simulates waiting for remote
    result = dict(remote="test_remote",
                  button="button_play")
    return result
