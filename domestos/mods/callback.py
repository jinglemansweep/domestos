from celery.task import task, subtask
from base import DTask
from mods.configurator import get_config


@task(base=DTask)
def test():

    return get_config.delay("test", 
                            callback=subtask(_test))


@task(base=DTask)
def _test(cfg):

    print "_test"
    print cfg

    return True
