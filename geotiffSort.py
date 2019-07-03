# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
Purpose: Sort clipped GeoTiff data to analysis directories
"""

__version__ = "$Revision: 1.1 $"[11:-2]
__date__ = "$Date: 2019/7/3 10:32:00 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
________________________________________________________
Author: Chris Zarzar
Created: 3 July 2019
Contact: chriszarzar@gmail.com

----History----

CREATED: Chris Zarzar 3-jul-2019
_______________________________________________________

"""

#Import dependencies 
import os
from os import path
import datetime
import shutil

#Set up required paths
wrkdir = "C:/Users/zarzarc/OneDrive/Desktop/Research/WFU/surface-atmosphere/se-precip/data/sample_mpe/"
os.chdir(wrkdir)
#os.getcwd()

#Check that required directories exist in wrkdir and create new directory if they do not exist
def ensure_dir(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

#Check for annual analysis dirs
directory = wrkdir+'annual_anl/'
ensure_dir(directory)
for year in range (2003, 2020):
    ensure_dir(directory+str(year))

#Check for seasonal analysis dirs 
directory = wrkdir+'simpseasonal_anl/'   
ensure_dir(directory)
for season in ['winter', 'spring', 'summer', 'fall']:
    ensure_dir(directory+season)
    
#Check for seasonal analysis dirs 
directory = wrkdir+'trueseasonal_anl/'   
ensure_dir(directory)
for season in ['winter', 'spring', 'summer', 'fall']:
    ensure_dir(directory+season)
    
#Check for diurnal analysis dirs
directory = wrkdir+'diurnal_anl/'
ensure_dir(directory)
hourList = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
for hour in hourList:
    ensure_dir(directory+hour)
    
#Check for NLCD analysis dir
directory = wrkdir+'nlcd_anl/'
ensure_dir(directory)
nlcdList = [2001, 2004, 2006, 2008, 2011, 2013, 2016]
for nlcd in nlcdList:
    ensure_dir(directory+str(nlcd))
    
#Check for SSC analysis dirs
directory = wrkdir+'ssc_anl/'
ensure_dir(directory)
sscList = ['dm', 'dp', 'dt', 'mm', 'mp', 'mt', 't', 'miss']
for ssc in sscList:
    ensure_dir(directory+ssc)



#Sort and copy NC data for diurnal analysis

#Set up a for loop to run through all files in dataset 
diurnalPath=wrkdir+'diurnal_anl/'
for dirName, subdirList, fileList in os.walk(wrkdir):
    for filename in fileList:
        if filename.endswith('.tif'):       
            if "NC" and ".01h" in filename: #Limit the analysis to North Carolina hourly files
                fname = filename
                fpath = (dirName+'/'+fname) #Get file path for copying the file later
                fnameBase = os.path.splitext(filename)[0] #Remove the extension for more easier datetime extraction
                dateName = fnameBase[7:-4] #Extract the date portion of the file name string
                DB_TIME_FORMAT = '%Y%m%d%H' #Set up the formatting of the string date in the file name
                date = datetime.datetime.strptime(dateName, DB_TIME_FORMAT) #interpret the date time from the string
                for hour in hourList: #Compare the file with the list of possible hourly output
                    hourStr = datetime.datetime.strptime(hour, '%H').strftime('%H') #Format the hour appropriately for moving the file to the correct directory
                    try:       #This simply avoids breaking of the script once it gets back seeing the same file using the os.walk method since I do not allow overwriting             
                        if date.hour==int(hour): #Using date.hour will give give 0 instead of 00, so it is fine to use int(hour) to reduce complexity of the script
                            shutil.copy2(fpath, diurnalPath+hourStr) #Copy the file to the appropriate directory
                            print (fname + ' copied to ' + diurnalPath+hourStr)
                    except:
                        pass
                        

#Sort and copy NC data for annual analysis

#Set up a for loop to run through all files in dataset                
annualPath=wrkdir+'annual_anl/'
for dirName, subdirList, fileList in os.walk(wrkdir):
    for filename in fileList:
        if filename.endswith('.tif'):       
            if "NC" and ".01h" in filename: #Limit the analysis to North Carolina hourly files
                fname = filename
                fpath = (dirName+'/'+fname) #Get file path for copying the file later
                fnameBase = os.path.splitext(filename)[0] #Remove the extension for more easier datetime extraction
                dateName = fnameBase[7:-4] #Extract the date portion of the file name string
                DB_TIME_FORMAT = '%Y%m%d%H' #Set up the formatting of the string date in the file name
                date = datetime.datetime.strptime(dateName, DB_TIME_FORMAT) #interpret the date time from the string
                for yearInt in range (2003, 2020): #Compare the file with the list of possible yearly output
                    yearStr = str(yearInt) #Needs to be in string format for both datetime command below and for setting up the directory
                    year = datetime.datetime.strptime(yearStr, '%Y').year #Format the year appropriately for moving the file to the correct directory
                    try:
                        if date.year==yearInt: #Compare file date with the year loop
                            shutil.copy2(fpath, annualPath+yearStr) #Copy the file to the appropriate directory
                            print (fname + ' copied to ' + annualPath+yearStr)
                    except:
                        pass
             
                
#Sort and copy NC data for simplified (JJA) seasonal analysis

#Set up a for loop to run through all files in dataset 
simpseasonalPath=wrkdir+'simpseasonal_anl/'                    
for dirName, subdirList, fileList in os.walk(wrkdir):
    for filename in fileList:
        if filename.endswith('.tif'):       
            if "NC" and ".01h" in filename: #Limit the analysis to North Carolina hourly files
                fname = filename
                fpath = (dirName+'/'+fname) #Get file path for copying the file later
                fnameBase = os.path.splitext(filename)[0] #Remove the extension for more easier datetime extraction
                dateName = fnameBase[7:-4] #Extract the date portion of the file name string
                DB_TIME_FORMAT = '%Y%m%d%H' #Set up the formatting of the string date in the file name
                date = datetime.datetime.strptime(dateName, DB_TIME_FORMAT) #interpret the date time from the string
                if 1==date.month or 2==date.month or 12==date.month:
                    print (fname)
                    #copy to winter folder
                elif 3==date.month or 4==date.month or 5==date.month:
                    #copy to spring folder
                elif 6==date.month or 7==date.month or 8==date.month:
                    #copy to summer folder
                elif 9==date.month or 10==date.month or 11==date.month:
                    #copy to fall folder
                    

#Sort and copy NC data for true calendar date seasonal analysis

"""
VERNAL EQUINOX.....(SPRING) MAR 20 2019 
SUMMER SOLSTICE....(SUMMER) JUN 21 2019 
AUTUMNAL EQUINOX...(FALL) SEP 23 2019 
WINTER SOLSTICE....(WINTER) DEC 21 2019  
"""
#Set up a for loop to run through all files in dataset 
trueseasonalPath=wrkdir+'trueseasonal_anl/'                    
for dirName, subdirList, fileList in os.walk(wrkdir):
    for filename in fileList:
        if filename.endswith('.tif'):       
            if "NC" and ".01h" in filename: #Limit the analysis to North Carolina hourly files
                fname = filename
                fpath = (dirName+'/'+fname) #Get file path for copying the file later
                fnameBase = os.path.splitext(filename)[0] #Remove the extension for more easier datetime extraction
                dateName = fnameBase[7:-4] #Extract the date portion of the file name string
                DB_TIME_FORMAT = '%Y%m%d%H' #Set up the formatting of the string date in the file name
                date = datetime.datetime.strptime(dateName, DB_TIME_FORMAT) #interpret the date time from the string
                if 1<= (gpsOut[2]- 84.1) <=16:date.month 
            #Will need to extract the month and data and use that to sort into the appropriate season directory            
            
#Sort and copy NC data for NLCD analysis

#Set up a for loop to run through all files in dataset                
for dirName, subdirList, fileList in os.walk(wrkdir):
    for filename in fileList:
        if filename.endswith('.tif'):
            if "NC" in filename:
                fname=filename
                print(fname)    
                #Will need to extract the year and will sort the data into directories that correspond to the date of the NLCD datasets

            

            
                
#Sort and copy NC data for SSC analysis

#Set up a for loop to run through all files in dataset                
for dirName, subdirList, fileList in os.walk(wrkdir):
    for filename in fileList:
        if filename.endswith('.tif'):
            if "NC" in filename:
                fname=filename
                print(fname)   
                #Script will need to compare fname with the SSC list and then take the classification as the method to sort the file into the appropriate directory
            
            
            
            