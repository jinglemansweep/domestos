from datetime import timedelta

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST= ""

CELERY_RESULT_BACKEND = "amqp"

CELERY_IMPORTS = ("plugins.echo.tasks",)

CELERYBEAT_SCHEDULE = {
    "runs-every-second": {
        "task": "plugins.echo.tasks.echo",
        "schedule": timedelta(seconds=1),
        "args": ("Hello",)
    },
    "runs-every-second-again": {
        "task": "plugins.echo.tasks.echo",
        "schedule": timedelta(seconds=1),
        "args": ("World",)
    }
}
