from datetime import timedelta

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST= ""

CELERY_RESULT_BACKEND = "amqp"

CELERY_IMPORTS = (
    "plugins.heartbeat.tasks", 
    "plugins.test.tasks",
    "plugins.cls.tasks",
)

CELERYBEAT_SCHEDULE = {
    "heartbeat.10s": {
        "task": "plugins.heartbeat.tasks.echo",
        "schedule": timedelta(seconds=10),
        "args": (10,)
    },
    "heartbeat.1m": {
        "task": "plugins.heartbeat.tasks.echo",
        "schedule": timedelta(seconds=60),
        "args": (60,)
    },
    "test.send_task": {
        "task": "plugins.test.tasks.test_send_task",
        "schedule": timedelta(seconds=10),
        "args": ("plugins.heartbeat.tasks.echo", [999])
    },
    "cls.test": {
        "task": "plugins.cls.tasks.TestThing",
        "schedule": timedelta(seconds=2),
        "args": ("Hello",)
    }
}

