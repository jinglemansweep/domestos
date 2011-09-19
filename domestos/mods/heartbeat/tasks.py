import sys
from datetime import timedelta
from celery.task import task, periodic_task
from base import DTask

print sys.path


@periodic_task(base=DTask,
               run_every=timedelta(seconds=5),
               ignore_result=True)
def heartbeat_periodic():
    logger = heartbeat_periodic.get_logger()
    logger.info("Heartbeat (%i seconds)" % (60))
