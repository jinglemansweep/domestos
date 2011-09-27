class DomestosRouter(object):

    """ Default task router """

    def route_for_task(self, task, args=None, kwargs=None):

        """ Task routing helper """

        parts = task.split(".")
        queue = "%s" % (parts[1])

        route = dict(queue=queue)
                    
        print route
        return route




    
