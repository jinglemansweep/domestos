import os
import sys

BASE_DIR = os.path.dirname(__file__)
MODULES_DIR = os.path.join(BASE_DIR, "mods")

sys.path.append(BASE_DIR)
INSTALLED_APPS = "domestos"

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = ""

CELERY_RESULT_BACKEND = "amqp"
CELERY_CACHE_BACKEND = "memcached://127.0.0.1:11211/"

CELERY_QUEUES = {"default": {"exchange": "default", "binding_key": "default"}}
CELERY_DEFAULT_QUEUE = "default"
CELERY_ROUTES = ("routers.DomestosRouter", )

task_imports = ["mods.%s.tasks" % (m) \
           for m in os.listdir(MODULES_DIR) \
           if os.path.isdir(os.path.join(MODULES_DIR, m)) \
           and os.path.exists(os.path.join(MODULES_DIR, m, "tasks.py"))]
CELERY_IMPORTS = tuple(task_imports)

