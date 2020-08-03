# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 13:05:40 2020

@author: Daria
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature

birddata = pd.read_csv(r'C:/Users/Daria/Documents/PythonScripts/bird_tracking.csv')
plt.figure(figsize=(7,7))
bird_names = pd.unique(birddata.bird_name)
# =============================================================================
#  
# for bird in bird_names:
#     ix=birddata.bird_name==bird
#     x,y = birddata.longitude[ix], birddata.latitude[ix]    
#     plt.plot (x,y, '.', label=bird)
#     
# plt.xlabel('Latitude')
# plt.ylabel("Longitude")
# plt.legend(loc='lower right')
# plt.savefig('bird_lat.pdf')
# =============================================================================
for bird in bird_names:
    ix=birddata.bird_name==bird
    speed = birddata.speed_2d[ix]
    ind = np.isnan(speed)
    plt.hist(speed[~ind], bins =np.linspace(0,30,20), density = True)
plt.xlabel('2d speed')
plt.ylabel('Frequency')
plt.savefig('bird_speed.pdf')

birddata.speed_2d.plot(kind ='hist', range=[0,20])

timestamps = []
for k in range(len(birddata)):
    timestamps.append(datetime.datetime.\
                      strptime(birddata.date_time.iloc[k][:-3], '%Y-%m-%d %H:%M:%S'))
birddata["timestamps"]=pd.Series(timestamps, index= birddata.index) 
#appended timestamps to existing pd.dataframe

eric_times = birddata.timestamps[birddata.bird_name=='Eric']
sanne_times = birddata.timestamps[birddata.bird_name=='Sanne']
elapsed_time = [time - eric_times[0] for time in eric_times]
elapsed_days= np.array(elapsed_time)/datetime.timedelta(days=1)
next_day = 1
inds = []
daily_mean_speed = []

for i, t in enumerate(elapsed_days):
    if t < next_day:
        inds.append(i)
    else:
        daily_mean_speed.append(np.mean(birddata.speed_2d[inds]))
        inds.append(i)
        next_day +=1
        
plt.figure(figsize=(10,10))
plt.plot(daily_mean_speed)
plt.xlabel('Day')
plt.ylabel('Mean speed')

proj = ccrs.Mercator()
plt.figure(figsize=(10,10))
ax=plt.axes(projection = proj)
ax.set_extent((-25.0, 20.0, 52.0, 10.0))
for bird in bird_names:
     ix=birddata.bird_name==bird
     x,y = birddata.longitude[ix], birddata.latitude[ix]
     ax.plot(x,y, '.', transform=ccrs.Geodetic(), label=bird)

