
import config ##custom config file to load API Keys

import csv
import pandas as pd
import numpy as np
import time

from collections import defaultdict

# from geopy.exc import GeocoderTimedOut
# from geopy.exc import GeocoderQuotaExceeded
# from geopy.exc import GeopyError
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

import plotly
import plotly.graph_objs as go
import plotly.plotly as py

from datetime import datetime


plotly.tools.set_credentials_file(username=config.plotly_username, api_key=config.plotly_api_key)



startTime = time.time()


searchTweet = "#OntarioTech"
# searchTweet = "#ONBudget"
# searchTweet = "#pakistan_Zindabad"
getGeoData = 1


df = pd.read_csv('data/'+searchTweet+'_tweets.csv')


# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(df['Location'])



if (getGeoData):

    locationList = df['Location'].tolist()
    for l in range(len(locationList)):
        locationList[l] = str(locationList[l])
    locationDict = defaultdict()

    for i in range(len(locationList)):
        if (locationList[i]== "nan"):
            pass
        else:
            locationDict.setdefault(locationList[i],[]).append(i)
    print("number of original keys = ",len(locationList))
    print("number of keys = ",len(locationDict.keys()))



    # geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    locationDictCoord = defaultdict()

    for loc in locationDict.keys():
        # print("key-",loc)
        geolocator = Nominatim(user_agent="twitterHashtagLocationGeocoding")
        a = geolocator.geocode(loc, exactly_one=True,timeout =3)
        # print(a)
        if a == None:
            pass
        else:
            locationDictCoord.setdefault(loc,[]).append(a.latitude)
            locationDictCoord.setdefault(loc,[]).append(a.longitude)

    # print(locationDict)
    # print(locationDictCoord)
    print("number of keys without diplicates = ",len(locationDictCoord.keys()))

    df['Latitude'] = np.nan
    df['Longitude'] = np.nan

    for keys in locationDictCoord.keys():
        # print("keys =", keys)
        if keys == '':
            # print("nan case keys = ", keys)
            pass
        else:
            for ind in locationDict[keys]:
                # print(ind)
                # print("---------",locationDictCoord[keys][0])
                df.loc[ind,'Latitude'] = locationDictCoord[keys][0]
                df.loc[ind,'Longitude'] = locationDictCoord[keys][1]


    # print(df.loc[:, ['Location', 'latitude','longitude']])


    df['text'] = df['Username'] + ' - ' + df['Location']

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



endTime = time.time()

print("running time= ",endTime-startTime)



#
# filename = 'name'
# from flask import Flask, render_template
#
# app = Flask(__name__)
#
# @app.route("/")
# def home():
#     return render_template("index.html")
#
# @app.route('/analysis')
# def analysis():
#     x = df
#     y = searchTweet
#     return render_template("analysis.html", data=x.to_html(index=False,border=False,classes='table table-responsive-sm table-sm table-striped'), name = y)
#
# if __name__ == "__main__":
#     app.run(debug=True)










# #Export Data to a csv
# df.to_csv('data.csv', index=False)


# users = df['Username'].tolist()
# print(users)
