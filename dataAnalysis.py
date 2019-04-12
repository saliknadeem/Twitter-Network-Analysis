
import config ##custom config file to load API Keys

import csv
import pandas as pd
import numpy as np


from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.exc import GeopyError



# import plotly.plotly as py
# import plotly.graph_objs as go
# from datetime import datetime
#

import plotly
plotly.tools.set_credentials_file(username=config.plotly_username, api_key=config.plotly_api_key)

searchTweet = "#ONBudget"
# searchTweet = "#pakistan_Zindabad"


df = pd.read_csv('data/'+searchTweet+'_tweets.csv')


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df['Location'])


# data = [go.Scatter(x=df.Date, y=df['Date'])]
# py.plot(data, filename = 'time-series-simple')


# geolocator = Nominatim()
# for loc in df['Location']:
#     try:
#         #print(loc)
#         location = geolocator.geocode(loc)
#         #print(location)
#         lat_long = {
#             "type": "Point",
#             "coordinates": [location.longitude, location.latitude]
#         }
#         print("loc=",loc," -- ",location.longitude,location.latitude)
#     except (GeopyError, AttributeError):
#         pass


from geopy.extra.rate_limiter import RateLimiter
# geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
#Function used to geocode locations and override timeout error
def do_geocode(address):
    geolocator = Nominatim(timeout=5)
    try:
        print("trying")
        return RateLimiter(geolocator.geocode(address,exactly_one=True), min_delay_seconds=5)
        # return geopy.geocode(address,exactly_one=True,timeout=None)
    except GeocoderTimedOut:
        print("exception")
        return do_geocode(address)

#Creating Geocoded Location column
df['GeocodedLocation']=df['Location'].apply(lambda x: do_geocode(x) if x != None else None)
print("done geocoding")

#Create the Latitude Column
lat=[]
for i in df['GeocodedLocation']:
    if i== None:
        lat.append(None)
    else:
        lat.append(i.latitude)
df['Latitude']=lat
df['Latitude'].astype('float')

#Create the Longitude Column
long=[]
for i in df['GeocodedLocation']:
    if i== None:
        long.append(None)
    else:
        long.append(i.longitude)
df['Longitude']=long
df['Longitude'].astype('float')


#Drop GeocodedLocation Column
df=df.drop(['GeocodedLocation'],axis=1)

print(df)



import plotly.graph_objs as go
import plotly.plotly as py

df['text'] = df['Username'] + '' + df['Location']

scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
    [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]

data = [ dict(
        type = 'scattergeo',
        locationmode = 'country names',
        lon = df['Longitude'],
        lat = df['Latitude'],
        text = df['text'],
        mode = 'markers',
        marker = dict(
            size = 8,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'circle',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            colorscale = scl,
            cmin = 0,
            color = 0.5,
            # color = df_sum_arrivals['cnt'],
            cmax = 1,
            # cmax = df_sum_arrivals['cnt'].max(),
            # colorbar=dict(
            #     title="Number of Tweets"
            # )
        ))]

layout = dict(
        title = 'Tweets Based on available locaiton data',
        colorbar = False,
        # colorbar = True,
        geo = dict(
            # scope='usa',
            projection= go.layout.geo.Projection(
            type = 'equirectangular'),
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5
        ),
    )

fig = dict( data=data, layout=layout )
url = py.plot( fig, validate=False, filename='tweets' )






# #Export Data to a csv
# df.to_csv('data.csv', index=False)


# users = df['Username'].tolist()
# print(users)
