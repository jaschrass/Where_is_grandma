# Gets icao numbers and other information for planes over US
# IMPORTANT!!!! Remember to wait the 15 second time limit when testing ;)

from opensky_api import OpenSkyApi, StateVector, OpenSkyStates
from datetime import datetime, date
import calendar
import time
import numpy as np
'''
YEAR = 2018
MONTH = 12
DAY = 12
d = datetime(YEAR, MONTH, DAY)
t = calendar.timegm(d.timetuple())
t2 = time.mktime(d.timetuple())
'''


for i in np.linspace(0, 50, 51):
    now = int(time.time())
    # t = 1544729313
    api = OpenSkyApi()
    # bbox = (min latitude, max latitude, min longitude, max longitude)
    states = api.get_states(time_secs=now)
    print(i, type(states))
    time.sleep(10)
for s in states.states:
    print("(%r, %r, %r, %r, %r)" % (s.longitude, s.latitude, s.baro_altitude,
                                    s.velocity, s.icao24))
