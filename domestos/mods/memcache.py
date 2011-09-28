import memcache
from celery.task import task, subtask
from base import DTask
from mods.configurator import get_config

@task(base=DTask)
def set(key, value):

    return get_config.delay("memcache", 
                            callback=subtask(_set, args=(key, value)))


@task(base=DTask)
def _set(cfg, key, value):

    print "cfg: " + cfg
    print "key: " + key
    print "value: " + value

    return True

    # mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    # mc.set("some_key", "Some value")
    # value = mc.get("some_key")
    # mc.set("another_key", 3)
