#!/usr/bin/python
import datetime
import json

tim = str(datetime.datetime.now())
print json.dumps({
       "time":tim
       })

