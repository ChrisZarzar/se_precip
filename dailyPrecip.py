# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
Purpose: Calculate 24 h accumulated precip from GeoTiffs and plot
"""

__version__ = "$Revision: 1.1 $"[11:-2]
__date__ = "$Date: 2019/7/1 14:10:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
________________________________________________________
Author: Chris Zarzar
Created: 1 July 2019
Contact: chriszarzar@gmail.com

----History----

CREATED: Chris Zarzar 1-jul-2019
_______________________________________________________

"""

#Import external libraries
from osgeo import gdal
from osgeo.gdalnumeric import *
from osgeo.gdalconst import *
import os
import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

wrkdir = "C:/Users/chris/OneDrive/Desktop/Research/WFU/surface-atmosphere/urban-precip/data/sample_mpe/20190405/"
os.chdir(wrkdir)
#os.getcwd()

#Set up a for loop to run through all files in dataset '
for dirName, subdirList, fileList in os.walk(wrkdir):
    for hour in range (24):
        fname = 'ST4.20190405%2.2d.01h.tiff' % hour
        #Open existing dataset '
        ds = gdal.Open(fname)
        #Accumulate precip for 24 hours '
        precipBand = ds.GetRasterBand(1)
        precipValues = BandReadAsArray(precipBand)
        precipValues[precipValues==9999]=numpy.nan
        if hour == 0:
            precipAcc = precipValues
            continue
        else:
            precipAcc += precipValues
#Replace nan with 9999
findnan = isnan(precipAcc)
precipAcc[findnan] = float(9999)



#Write the out file
driver = gdal.GetDriverByName("GTiff")
dsOut = driver.Create("ST4.20190405.tiff", ds.RasterXSize, ds.RasterYSize, 1, precipBand.DataType)
CopyDatasetInfo(ds,dsOut)
bandOut=dsOut.GetRasterBand(1)
BandWriteArray(bandOut, precipAcc)

##Close the datasets
precipValues = None
ds = None
bandOut = None
dsOut = None     
        
        
"""       
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
"""