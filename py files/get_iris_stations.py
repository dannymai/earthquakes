from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import sys
import time as ti

import numpy as np
import os


file = 'station_info.txt'

clients = ['IRIS']


# Define parameters
time = UTCDateTime('1994-01-01T00:00:00.001')

starttime = time
endtime = UTCDateTime('2022-01-01T00:00:00.001')
net = "C*"
stn = "*"
channel = "*"
count = 0
lst = []

# Timing the code execution
start = ti.time()
for cl in clients:
    try:
        print(f"--> Trying for client: {cl}")
        client = Client(cl)

        inventory = client.get_stations(network=net, station=stn, channel=channel,
                                        minlatitude = 32.5, maxlatitude = 34.5,
                                        minlongitude = -119.75, maxlongitude = -114.9,
                                        level="response", starttime=starttime, endtime=endtime)
        

        f_path = os.path.join(os.getcwd(), cl + '_' + file)
        
        if inventory not in lst:
            print(inventory)
            
            lst.append(inventory)
            # OUTPUT STATION DATA TO A TEXT FILE TO IMPORT BELOW 
            inventory.write(f_path, format='STATIONTXT',level='station')
            
        end = ti.time()
            
            
        print(f"The program took {end-start} seconds to run")

    except:
        print(f'Failed to try ---- {cl} \n', sys.exc_info())

        
    count += 1
"""OUTPUT A TEXT FILE TO STORE STATION DATA"""
