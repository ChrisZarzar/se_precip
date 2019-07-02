# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
Purpose: Convert grib to GeoTiff
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

#Import gdal
from osgeo import gdal
import os

wrkdir = "C:/Users/chris/OneDrive/Desktop/Research/WFU/surface-atmosphere/urban-precip/data/sample_mpe/20190405/"
os.chdir(wrkdir)
#os.getcwd()

#Set up a for loop to run through all files in dataset '
for dirName, subdirList, fileList in os.walk(wrkdir):
    for fname in fileList:
        if fname.endswith(".01h"):
        
            #Open existing dataset '
            src_ds = gdal.Open(fname)
            
            #Open output format driver, see gdal_translate --formats for list
            format = "GTiff"
            driver = gdal.GetDriverByName( format )
            
            #Output to new format
            dst_ds = driver.CreateCopy(fname+".tiff", src_ds, 0 )
            
            #Properly close the datasets to flush to disk
            dst_ds = None
            src_ds = None
