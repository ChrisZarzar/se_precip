# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
Purpose: Calculate 24 h accumulated precip from GeoTiffs and plot

Notes: You will want to run this script from the parent "/clipped_mpe/" directory
        "/clipped_mpe/" must be the GeoTIFF converted and clipped files. 
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

CREATED:1-jul-2019,  Chris Zarzar 

EDITED: 5-jul-2019, Chris Zarzar
-- Adjust script so that it can loop through entire directories and write out
daily total precipitation to the current working directory by testing whether the 
day is equivalent to the previous day. 
_______________________________________________________

"""

#Import external libraries
from osgeo import gdal
from osgeo.gdalnumeric import *
from osgeo.gdalconst import *
import os
import numpy

# Set up main working directory
#myPath = os.path.abspath(os.path.relpath('/.')) #trying to set up a relative path
#wrkdir = os.path.join(myPath, os.path.relpath('/./sample_mpe/'))#trying to set up a relative path
wrkDir = "C:/Users/zarzarc/OneDrive/Desktop/Research/WFU/surface-atmosphere/se-precip/data/sample_mpe/20190405" #For running in test mode
os.chdir(wrkDir) #For running in test mode
#wrkDir = os.getcwd() #For running operationally

#Open up log files
f = open("errLog.txt", "w+")


#Set up a for loop to run through all files in dataset '
for year in range (2003, 2020):
    for month in range (1,13):
        for day in range (1,32):
            for hour in range (24):
                try:
                    fname = 'NC_ST4.%4.4d%2.2d%2.2d%2.2d.01h.tif' % (year, month, day, hour) #.01h is important to limit the calculation to hourly data
                    filePath = wrkDir + '/' + fname 
                    if not os.path.exists(filePath):
                        f.write(fname+" does not exist \n") #list dates that obviously should not exist, but also data that might be missing from the dataset
                        continue
                    else: 
                        pass 
                    ds = gdal.Open(fname) #Open raster
                    #Accumulate precip for 24 hours to calculate daily total precip
                    precipBand = ds.GetRasterBand(1)
                    precipValues = BandReadAsArray(precipBand)
                    precipValues[precipValues==9999]=numpy.nan
                    if hour == 0:
                        precipAcc = precipValues #Set up first array for summation of daily total precip
                        continue
                    else:
                        precipAcc += precipValues #Add current time to daily total precip
                        if hour == 23: 
                            #Write the out file
                            findnan = isnan(precipAcc) #Replace nan with 9999
                            precipAcc[findnan] = float(9999)
                            driver = gdal.GetDriverByName("GTiff")
                            dsOut = driver.Create("NC_ST4.%4.4d%2.2d%2.2d00.day.tif" % (year, month, day), ds.RasterXSize, ds.RasterYSize, 1, precipBand.DataType)  
                            CopyDatasetInfo(ds,dsOut)
                            bandOut=dsOut.GetRasterBand(1)
                            BandWriteArray(bandOut, precipAcc)    
                        else:
                            continue
                except:
                    pass
##Close the datasets
precipValues = None
ds = None
bandOut = None
dsOut = None     
f.close()
