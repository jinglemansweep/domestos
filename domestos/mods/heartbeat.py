import sys
from datetime import timedelta
from celery.task import task, periodic_task


@periodic_task(run_every=timedelta(seconds=60))
def heartbeat_periodic():
    logger = heartbeat_periodic.get_logger()
    logger.info("Heartbeat (%i seconds)" % (60))

