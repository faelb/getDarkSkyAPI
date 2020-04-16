"""
    File name: getAPI.py
    Author: faelb (faelb@gmx.at)
    Date created: 16/04/2020
    Date last modified: 16/04/2020
    Python Version: 3.8
   This program fetches data from the DarkSkyAPI
   to create dummy-data for our SMAROO db.
"""

import mysql.connector
from darksky.api import DarkSky, DarkSkyAsync
from darksky.types import languages, units, weather
from datetime import datetime as dt  # for timemachine API

API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
darksky = DarkSky(API_KEY)

mydb = mysql.connector.connect(
    host="localhost",
    user="faelb",
    passwd="faelb",
    database="smaroo_db"
)
myCursor = mydb.cursor()
format = '%Y-%m-%d %H:%M:%S'
for i in range(2, 30):
    t = dt(2020, 2, i, 3, 0, 0)  # for some reason the API gives day -1 thats why we start at 2 to 30

    latitude = 48.210033
    longitude = 16.363449
    forecast = darksky.get_time_machine_forecast(
        latitude, longitude,
        extend=False,  # default `False`
        lang=languages.ENGLISH,  # default `ENGLISH`
        values_units=units.SI,  # default `auto`
        exclude=[weather.MINUTELY, weather.ALERTS],  # default `[]`,
        timezone='GMT',  # default None - will be set by DarkSky API automatically
        time=t
    )

    for item in forecast.daily:
        a = item.time
        b = item.apparent_temperature_high
        c = item.humidity

    sql = "INSERT INTO temperatur (Zeitpunkt, temperatur) VALUES (%s, %s)"
    values = (a.strftime(format), int(b))
    myCursor.execute(sql, values)
    sql = "INSERT INTO humidity (Zeitpunkt, humidity) VALUES (%s, %s)"
    values = (a.strftime(format), c)
    myCursor.execute(sql, values)

    mydb.commit()

print("Fertig")

# print(forecast.latitude)
# print(forecast.longitude)
# print(forecast.timezone)

# [print(i.apparent_temperature_high) for i in forecast.daily] #because daily is a list (but with only one item?)
# print(len(forecast.daily.data)) #yes only one item in there - makes sense for a daily request
# print(f"temp: {forecast.currently.temperature}")


# print(mydb)
#
# myCursor.execute("SELECT * FROM temperatur")
#
# fetchresult = myCursor.fetchall()
#
# for x in fetchresult:
#     print(x)
