from celery.execute import send_task
from celery.task import task


@task
def test_send_task(task_id, task_args):
    result = send_task(task_id, task_args)
    print result
