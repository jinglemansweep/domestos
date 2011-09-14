from celery.task import task


@task
def echo(msg):
    print msg
    return msg


