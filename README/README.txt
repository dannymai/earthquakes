# earthquakes

# Project Goal: Retrieve earthquakes latitude, longitude, and hypocenter depth

# Descriptions of get_earthquakes.py file

- File get_earthquakes.py is used to retrieve multiple earthquakes from USGS web services [USGS Query method](https://earthquake.usgs.gov/fdsnws/event/1/); **default vicinity is Southern California**

- get_earthquakes.py contains three mode standard mode: static mode - used to retrieve existing earthquakes.csv file and display 10 retrieved earthquakes; scrape mode - used to scrape *user specified amount* of earthquakes and display them; default mode - used to scrape and write to earthquakes.csv file 

- git ignore for notebook files will be updated later


# Dependent modules:
- Pandas, Requests, datetime, threading, os, sys, time

''' Southern California default geographic coordinates

- lat: 32.5 to 34.5
- long: -119.75 to -114.9

'''
