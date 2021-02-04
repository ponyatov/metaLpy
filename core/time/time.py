## @file
## @brief generic date/time

from core.object import Object

import datetime as dt

## generic date/time
## @ingroup time
class Time(Object):
    def __init__(self, V=''):
        super().__init__(V)

## current local time
## @ingroup time
class LocalTime(Time):
    ## date, time, refresh period in ms
    ## @returns `{date,time,refresh:ms}`
    def json(self):
        now = dt.datetime.now()
        date = now.strftime('%d.%m.%Y')
        time = now.strftime('%H:%M:%S')
        return {"date": date, "time": time, "refresh": 60e3 / 1}
