# Gets data from excel sheet and searches for specific aircraft classes

import pandas as pd
import time
from datetime import datetime, date

YEAR = 2018
MONTH = 12
DAY = 13
d1 = date(YEAR, MONTH, DAY)
timestamp1 = time.mktime(d1.timetuple())

# get most recent aircraft data .csv file
'''
aircraft_data = pd.read_csv('https://opensky-network.org/datasets/metadata/' +
                            'aircraftDatabase.csv')
'''
# FIXME - for testing I'm using the aircraft data file i've already downloaded
fields = ['icao24', 'model']
aircraft_data = pd.read_csv("aircraftDatabase.csv", na_filter=False,
                            usecols=fields)

model_names = aircraft_data['model']
icaos = aircraft_data['icao24']
model_list = list(model_names)

# be as specific or as general as desired with the aircraft name
# its a good i
aircraft = '787'
name_check = [name for name in model_list if aircraft in name]
name_id = [model_list.index(x) for x in model_list if aircraft in x]

icao_num = []
for i in range(len(name_id)):
    icao_num.append(icaos[name_id[i]])
# its a good idea to glance at the name_check list to make only the desired
# aircraft type is found by the algorithm
print(name_check, icao_num)
