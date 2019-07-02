#! /usr/bin/python

''' Generate map of MPE data
'''

' Import external libraries (these will need to be installed) '
import numpy as np
import pygrib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

' Open input files and accumulate precip for 24 hours '
for hour in range (24):
    filename = 'ST4.20190405%2.2d.01h' % hour
    dataFile = pygrib.open (filename)
    msg = dataFile[1]
    if hour == 0:
        precip = msg['values']
        lats, lons = msg.latlons()
        continue
    else:
        precip += msg['values']
        
' Generate map of precipitation '
fig = plt.figure ()
map = Basemap (projection='lcc', lat_0=34.5, lon_0=-78, lat_1=33., lat_2=37., \
               llcrnrlon=-85., llcrnrlat=33., urcrnrlon=-75., urcrnrlat=37.5, \
               resolution='h', area_thresh=1000.)
map.drawcoastlines()
map.drawmapboundary()
map.drawcountries()
map.drawstates()
fig = map.contourf (lons, lats, precip, latlon='True')
cbar = map.colorbar (fig, location='right')
plt.title ('Daily Precip (mm)')
plt.savefig('NC_precip.png')
plt.close()
