'''
python file to do stuff with the opensky api
'''

from opensky_api import OpenSkyApi
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from threading import Timer
from time import sleep


# Not used right now but can be used to make a code stop and start
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def plot_planes_in_us(ims):
    api = OpenSkyApi()
    states = api.get_states(bbox=(13, 58, -144, -53))
    lat = []
    lon = []
    icao = []
    for s in states.states:
        '''
        print("(%r, %r, %r, %r, %r)" % (s.longitude, s.latitude,
                                        s.baro_altitude,
                                        s.velocity, s.icao24))
        '''
        lon.append(s.longitude)
        lat.append(s.latitude)
        icao.append(s.icao24)

    # plt.figure(figsize=(12, 6))
    m = Basemap(projection='merc', llcrnrlat=13, urcrnrlat=58,
                llcrnrlon=-144, urcrnrlon=-53, resolution='c')
    m.drawstates()
    m.drawcountries(linewidth=1.0)
    m.drawcoastlines()
    map_lon, map_lat = m(*(lon, lat))
    ims.append(m.plot(map_lon, map_lat, 'b.'))
    '''
    for i in range(len(icao)):
        if icao[i] == 'aa56b4':
            ims.append(m.plot(map_lon[i], map_lat[i], 'r.'))
            print('hi', icao[i])
    '''
    '''
        # Doesn't work, need a large if statement outside the loop checking if
        # the desired icao number exists
        else:
            ims.append(m.plot(map_lon, map_lat, 'b.'))
    '''
    # plt.show()
    return ims


ims = []
fig = plt.figure()
'''
rt = RepeatedTimer(1, plot_planes_in_us, ims)
try:
    sleep(5)
finally:
    rt.stop()
'''
i = 0
while i < 6:
    ims = plot_planes_in_us(ims)
    sleep(15)
    i += 1

'''
fig = Figure()
canvas = FigureCanvas(fig)
fig = plt.figure(figsize=(12, 6))
'''
ani = animation.ArtistAnimation(fig, ims, interval=1000, blit=False,
                                repeat_delay=(500))
ani.save('test_planes_in_us.gif', writer=PillowWriter())

plt.show()
