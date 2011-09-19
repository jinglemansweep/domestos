import os
import sys
import yaml


from mods.core.tasks import configure


def get_module_config(name):
    cfg = configure.apply()
    print cfg
    base_dir = os.path.dirname(__file__)
    filename = os.path.join(base_dir, "config.yml")
    if not os.path.exists(filename): return dict()
    stream = file(filename, "r")
    cfg = yaml.load(stream)
    return cfg


