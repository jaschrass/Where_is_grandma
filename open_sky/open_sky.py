'''
python file to do stuff with the opensky api
'''

from opensky_api import OpenSkyApi
import matplotlib.pyplot as plt
from time import sleep
from datetime import datetime
import pandas as pd


def find_icaos(aircraft):
    '''
    Finds the icao24 id #s of a desired aircraft type using the data from the
    current downloaded version of aircraftDatabase.csv. Requires an aircraft
    input as a string.
    Examples: 'A380', '737', '787'
    '''
    # be as specific or as general as desired with the aircraft name
    fields = ['icao24', 'model']
    aircraft_data = pd.read_csv("aircraftDatabase.csv", na_filter=False,
                                usecols=fields)

    model_names = aircraft_data['model']
    icaos = aircraft_data['icao24']
    model_list = list(model_names)

    name_id = [model_list.index(x) for x in model_list if aircraft in x]

    icao_num = []
    for i in range(len(name_id)):
        icao_num.append(icaos[name_id[i]])
    '''
    it's a good idea to glance at the name_check list to make only the desired
    aircraft type is found by the algorithm if using a aircraft name not
    listed in the examples above
    '''
    # name_check = [name for name in model_list if aircraft in name]
    # print(name_check, icao_num)
    return icao_num


def get_data(desired_icaos):
    api = OpenSkyApi()
    # bbox=(latmin,latmax,lonmin,lonmax) - selecting area over united states
    # time_secs=0 - time as unix time stamp or datetime in UTC
    # icao24=None - retrive state vectors for given ICAO24 addresses
    #   (input array of strings)

    # FIXME - set time_secs and icao24 arguments once a passowrd is obtained to
    # run at set times (for example the time when the aircraftDatabase was last
    # updated)
    states = api.get_states(
                            bbox=(13, 58, -144, -53))
    lat = []
    lon = []
    icao = []
    vel = []
    alt = []
    # print(states)
    for s in states.states:
        '''
        print("(%r, %r, %r, %r, %r)" % (s.longitude, s.latitude,
                                        s.baro_altitude,
                                        s.velocity, s.icao24))
        '''
        lon.append(s.longitude)
        lat.append(s.latitude)
        icao.append(s.icao24)
        vel.append(s.velocity)
        alt.append(s.geo_altitude)

    return lon, lat, icao, vel, alt


'''
# while loop to run for a period of time
i = 0
while i < 6:  # runs for 6 * 15 seconds
    desired_icaos = find_icaos('A380')
    [lat, lon, icao, vel, alt] = get_data(desired_icaos)
    sleep(15)  # wait for 15 seconds between runs
    i += 1
'''

# gets a list of icao numbers for the input aircraft type
desired_icaos = find_icaos('A380')
# print(desired_icaos)

# uses the api to output data for the desired icaos
[lat, lon, icao, vel, alt] = get_data(desired_icaos)
# print(lat, lon)

# Plotting Velocity Distribution
plt.hist(vel, 200)
plt.xlabel('Velocity (m/s)')
plt.ylabel('Number of Aircraft')
plt.title('Velocity Distribution of Aircraft over the US')
plt.show()
