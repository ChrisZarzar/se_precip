#! /usr/bin/ python
# coding=utf-8
"""
Purpose: This script will explore the MPE data supplied from Dr. Jamie Dyer.


"""
__version__ = "$Revision: 1.0 $"[11:-2]  # type: str
__date__ = "$Date: 2019/06/17 13:56:47 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
Author: Chris Zarzar
Notes: Dr. Dyer: Here’s a sample of the MPE data in gridded binary and csv format (the csv is the processed version).
The grib file only has one hour of data while the csv version has 24 hours of data.
Both files are compressed using the gzip utility.

Gridded binary – ST4.2018063012.01h
Comma separated – US_prcp_063018.dat
- This is supposed to be comma separated, but it appears it is fixed deliminated where each column is eight characters
To convert to CSV, first run this in bash: 
gawk '$1=$1' FIELDWIDTHS='8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8' OFS=, US_prcp_063018.dat > US_prcp_063018.csv
Then run this to add a header line for easy interpretation in R, ArcGIS, and QGIS
sed -i '1s/^/lon,lat,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23,t24\n/' US_prcp_063018_edited.csv


Requirements:
1. Numpy
________________________________________________________
#### HISTORY ####

17-jun-2019 [Chris Zarzar]: Created. Much of script adapted from Comp Methods and ECT scripts. 


______________________________________________________________________________
"""

# Import necessary external packages
import os
import pandas as pd

dataDir = "C:/Users/zarzarc/OneDrive/Desktop/Research/WFU/surface-atmosphere/se-precip/data/sample_mpe/"
os.chdir(dataDir)
inFile = "US_prcp_063018.dat"
# if data is not formatted as csv, run this code block
colWidth = [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]
df = pd.read_fwf(inFile, widths=colWidth)

# if data is formatted as csv, run this code block
inFile = "US_prcp_063018.csv"
df = pd.read_csv(inFile)


df.shape #inspect the shape of the data frame imported
df.ndim #inspect the number of dimensions in the data


# explore what percentage of the locations have no missing data
# below is the traditional python, and faster, way to open and explore the data
inputfile = 'US_prcp_063018.dat'
infile = open(inputfile, 'r')
infileList = infile.readlines()
infile.close()


count = 0
count2 = 0
for i in range(len(infileList)):
    rows = str(infileList[i][0:207])
    for j in range(16,207,8):
        columns = float(rows[j:j+8])
        if (columns == -999.000):
            break
        else:
            count += 1
gooddays = float(count/24)

percentage = (gooddays/len(infileList))*100

print "There are %.1f locations with no missing data" % (percentage)

# explore the average total daily precipitation during day with no missing data
count = 0
rainsum = 0
for i in range(len(infileList)):
    rows = str(infileList[i][0:207])
    for j in range(16,207,8):
        columns = float(rows[j:j+8])
        if (columns != -999.000):
            rainsum = rainsum+columns
            count += 1

avgprcp = float(rainsum)/(count/24)

print "The average daily total precipitation for days with non-missing data is %.3f mm" % (avgprcp)

# explore the total daily percipitation for a point of interest

rainsum = 0
for i in range(len(infileList)):
    lon = float(infileList[i][0:8])
    lat = float(infileList[i][9:15])
    rows = (infileList[i][0:207])
    if (lon == -88.821 and lat == 50.026):
        for j in range(16,207,8):
            columns = float(rows[j:j+8])
            if (columns != -999.000):
                rainsum = rainsum + columns

print "The total precipitation for the specified location is %.3f mm" % (rainsum)