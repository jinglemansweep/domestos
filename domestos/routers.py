class DomestosRouter(object):

    def route_for_task(self, task, args=None, kwargs=None):
        parts = task.split(".")
        module = parts[1]
        if parts[0] == "mods" and "periodic" not in parts[-1]:
            queue = "%s" % (module)
        else:
            queue = "default"
        return dict(queue=queue)


    
