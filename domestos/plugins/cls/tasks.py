from celery.task import Task

class TestThing(Task):

    def __init__(self):
        self.name = "Louis"
        self.count = 1

    def run(self, word):
        self.count = self.count + 1
        print "%s %s (%i)" % (word, self.name, self.count)

