from celery.decorators import task
from base import DTask

@task(base=DTask)
def echo(message):
 
    logger = echo.get_logger()
    logger.info(message)
    return message
