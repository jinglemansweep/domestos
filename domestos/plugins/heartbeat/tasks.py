from celery.task import task


@task
def echo(interval):
    print "Heartbeat (%i secs)" % (interval)



