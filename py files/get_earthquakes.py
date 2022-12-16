import pandas as pd
import requests
from datetime import date
from datetime import timedelta
import os
import time
import sys
import threading

file_name = 'earthquakes.csv'

done = False

def animate():
    
    while done is not True:
        sys.stdout.write(f'loading ------- \n')
        sys.stdout.flush()
        time.sleep(1)
        
#        sys.stdout.flush()
#        time.sleep(1)
        
        

    if done is True:
        sys.stdout.write('Done!     ')
        pass 



def static_mode(path):

    df = pd.read_csv(path)
    print(df.head(10))


def default_mode():
    year = int(input('Enter a year before 2010: '))
    month = int(input('Enter a month: '))
    day = int(input('Enter a day: '))



    # User input for query start time and convert them to standard time format based on FDSN
    da = date(year, month, day)
    starttime = da.strftime("%Y-%m-%d")
    yesterday = da + timedelta(days = 365*1)
    endtime = yesterday.strftime("%Y-%m-%d")

    main_web = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'

    # Southern California boundary box 
    minlatitude = 'minlatitude=32.5'
    maxlatitude = 'maxlatitude=34.5'
    minlongitude = 'minlongitude=-119.75'
    maxlongitude = 'maxlongitude=-114.9'

    limit = 'limit=' + input("Please enter number limit of earthquakes (recommended less than 19000): ")

    # Calling function to run a loop 
    threading.Thread(target=animate).start()



    paragms = ['format=geojson',f'starttime={starttime}',f'endtime={endtime}', 'eventtype=earthquake', (minlatitude), (maxlatitude), (minlongitude), (maxlatitude), 'orderby=time-asc', limit]

    web_str = main_web + '&'.join(paragms) 

    response = requests.get(web_str).json()

    # Generate data from web scrapping; get lat,long,depth
    coords = []
    location = []
    magnitudes = []
    for k,v in response.items():
        if k == "features":
            for i,each in enumerate(v):
                # Get the coordinates within "geometry" dict
                if "geometry" in each:
                    coords.append(each["geometry"]["coordinates"])
                    location.append(each["properties"]["title"])
                    magnitudes.append(each["properties"]["mag"])


    # Zipping the magnitude and location detail into a comprehensive list
    info = []
    for coord,mag in zip(coords, magnitudes):
        coord.insert(0, mag)
        # Create a new list
        info.append(coord)


    # Convert to dataframe
    headers = ["Magnitude", 'lat','long','depth (km)']
    df = pd.DataFrame(data = info, index=location, columns = headers)


    # Writing files to csv 
    f_path = os.path.join(os.getcwd(), file_name)
    df.to_csv(f_path)


    # reset done to True to stop threading 
    global done 
    done=True

    return print(df.head(10))

"""SCRAPING MODE DO NOT SCRAPE THE MAGNITUDE"""
def scrape_mode():

    today = date.today()
    print(f"Scrapping earthquakes data from 1 year ago to {today}")
    
    endtime = today.strftime("%Y-%m-%d")
    before = today - timedelta(days = 365*1)
    starttime = before.strftime("%Y-%m-%d")

    # Providing web URLs
    main_web = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'
    # Parameters to scrape 
    minlatitude = 'minlatitude=32.5'
    maxlatitude = 'maxlatitude=34.5'
    minlongitude = 'minlongitude=-119.75'
    maxlongitude = 'maxlongitude=-114.9'
    limit = 'limit=' + input("Please enter number limit of earthquakes (recommended less than 19000): ")

    
    # Setting parameters 
    paragms = ['format=geojson',f'starttime={starttime}',f'endtime={endtime}', 'eventtype=earthquake', (minlatitude), (maxlatitude), (minlongitude), (maxlatitude), 'orderby=time-asc', limit]

    web_str = main_web + '&'.join(paragms) 

    response = requests.get(web_str).json()

    # Generate data from web scrapping; get lat,long,depth
    coords = []
    location = []
    for k,v in response.items():
        if k == "features":
            for i,each in enumerate(v):
                # Get the coordinates within "geometry" dict
                if "geometry" in each:
                    coords.append(each["geometry"]["coordinates"])
                    location.append(each["properties"]["title"])


    # Convert to dataframe
    headers = ['lat','long','depth (km)']
    df = pd.DataFrame(data = coords, index=location, columns = headers)

    return print(df.head(5))



# Setting file running nature

import sys
if __name__ == "__main__":
    if len(sys.argv) == 1:
        default_mode()


    elif sys.argv[1] == '--static':
        try:
            path = str(sys.argv[2])

            static_mode(path)

        except:
            print("***PLEASE MAKE SURE TO ESCAPE SPACES IN PATH AND GIVE DATASET FILE NAME")
            print(sys.exc_info())

    elif sys.argv[1] == '--scrape':
        scrape_mode()


