class Schedule(object):

    def __init__(self, years=None, months=None, days=None, hours=None, minutes=None, seconds=None):
        
        if not years: years = list()
        if not months: months = list()
        if not days: days = list()
        if not hours: hours = list()
        if not minutes: minutes = list()
        if not seconds: seconds = list()

        self.years = years
        self.months = months
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

        
