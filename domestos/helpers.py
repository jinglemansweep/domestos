import datetime

daynames = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")

class DTCompare(object):

    def __init__(self, **kwargs):

        now = datetime.datetime.now()
        active = True
        if "year" in kwargs:
            if not now.year in kwargs["year"]: active = False
        if "month" in kwargs:
            if not now.month in kwargs["month"]: active = False
        if "day" in kwargs:
            if not now.day in kwargs["day"]: active = False            
        if "hour" in kwargs:
            if not now.hour in kwargs["hour"]: active = False
        if "minute" in kwargs:
            if not now.minute in kwargs["minute"]: active = False        
        if "second" in kwargs:
            if not now.second in kwargs["second"]: active = False
        if "dayofweek" in kwargs:
            if not now.isoweekday() in kwargs["dayofweek"]: active = False
        #logger.debug("DTCompare from %s:%s:%s on %s/%s/%s to %s:%s:%s on %s/%s/%s" % (params["start_hour"], params["start_minute"], params["start_second"], params["start_day"], params["start_month"], params["start_year"], params["finish_hour"], params["finish_minute"], params["finish_second"], params["finish_day"], params["finish_month"], params["finish_year"],))        
        self.active = active
        
    def is_active(self):

        return self.active
    
    def __str__(self):
        return str(self.is_active())

    
class DT(object):
    
    def __init__(self):
        now = datetime.datetime.now()
        self.dict = {
            "now": (now, now),
            "year": (now.year, now.year), 
            "month": (now.month, now.month), 
            "day": (now.day, now.day), 
            "hour": (now.hour, now.hour), 
            "minute": (now.minute, now.minute), 
            "second": (now.second, now.second),
            "dayofweek": (now.isoweekday(), ),
            "dayofweek_name": (daynames[now.isoweekday()-1], ),
            "weekday": now.isoweekday() in range(1, 5),
            "weekend": now.isoweekday() in range(6, 7),
        }
        
    def update(self):
        now = datetime.datetime.now()
        self.dict = {
            "now": (now, self.dict["now"][0]),
            "year": (now.year, self.dict["year"][0]), 
            "month": (now.month, self.dict["month"][0]), 
            "day": (now.day, self.dict["day"][0]), 
            "hour": (now.hour, self.dict["hour"][0]), 
            "minute": (now.minute, self.dict["minute"][0]), 
            "second": (now.second, self.dict["second"][0]),
            "dayofweek": (now.isoweekday(), ), 
            "dayofweek_name": (daynames[now.isoweekday()-1], ),            
            "weekday": now.isoweekday() in range(1, 5),
            "weekend": now.isoweekday() in range(6, 7),            
        }
    
    def get_value(self, unit):
        return self.dict["%s" % unit][0]
        
    def is_new(self, unit):
        is_new = not self.dict["%s" % unit][0] == self.dict["%s" % unit][1]
        return is_new    