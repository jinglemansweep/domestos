import os
import sys
import yaml
from socket import gethostname
from xdg import BaseDirectory
from celery.task import task
from base import DTask


@task(base=DTask)
def configure(app_name="domestos"):

    """ Read (or create) configuration files and directories """
    
    xdg_config = BaseDirectory.xdg_config_home
    xdg_cache = BaseDirectory.xdg_cache_home

    config_dir = os.path.join(xdg_config, app_name)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        
    cache_dir = os.path.join(xdg_cache, app_name)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        
    modules_dir = os.path.join(config_dir, "modules")
    if not os.path.exists(modules_dir):
        os.makedirs(modules_dir)

    app_config_filename = os.path.join(config_dir, "app.yml")

    if os.path.exists(app_config_filename):

        stream = file(app_config_filename, "r")
        cfg = yaml.load(stream)

    else:

        cfg = generate_default(config_dir,
                               cache_dir,
                               modules_dir)

        stream = file(app_config_filename, "w")
        yaml.dump(cfg, stream)
        
    stream.close()

    return cfg

    
def generate_default(config_dir,
                     cache_dir,
                     modules_dir):

    """ Generate default configuration """

    cfg = {
        "general": {
            "name": gethostname(),
            "config_dir": config_dir,
            "cache_dir": cache_dir
        },
        "amqp": {
            "host": "localhost",
            "port": 5672,
            "username": "guest",
            "password": "guest"
        }
    }

    return cfg


configure.apply()

