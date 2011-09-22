import os
import sys
import yaml
from celery.task import task, subtask
from base import DTask
from utils import configure


@task(base=DTask)
def get_configuration(key, callback=None):
    cfg = configure()
    config_dir = cfg.get("general").get("config_dir")
    filename = os.path.join(config_dir, key + ".yml")
    if not os.path.exists(filename): return dict()
    stream = file(filename, "r")
    cfg = yaml.load(stream)
    if callback is not None:
        subtask(callback).delay(cfg)
    return cfg
