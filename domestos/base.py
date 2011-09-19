from celery.task import Task

class DTask(Task):

    abstract = True

    def __call__(self, *args, **kwargs):

        # print "Do Stuff Before Task Run"
        return self.run(*args, **kwargs)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):

        # print "Do Stuff After Task Run"
        pass



