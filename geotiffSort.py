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
        if filename.endswith('.tif') or filename.endswith('.tiff'):       
            if "NC" in filename and ".01h" in filename: #Limit the analysis to North Carolina hourly files
                fname = filename
                fpath = (dirName+'/'+fname) #Get file path for copying the file later
                fnameBase = os.path.splitext(filename)[0] #Remove the extension for more easier datetime extraction
                dateName = fnameBase[7:-4] #Extract the date portion of the file name string
                DB_TIME_FORMAT = '%Y%m%d%H' #Set up the formatting of the string date in the file name
                date = datetime.datetime.strptime(dateName, DB_TIME_FORMAT) #interpret the date time from the string
                for hour in hourList: #Compare the file with the list of possible hourly output
                    hourStr = datetime.datetime.strptime(hour, '%H').strftime('%H') #Format the hour appropriately for moving the file to the correct directory
                    try:       #This simply avoids breaking of the script once it gets back seeing the same file using the os.walk method since I do not allow overwriting             
                        if int(date.hour)==int(hour): #Using date.hour will give give 0 instead of 00, so it is fine to use int(hour) to reduce complexity of the script
                            shutil.copy2(fpath, diurnalPath+hourStr) #Copy the file to the appropriate directory
                    except:
                        pass
                        

#Sort and copy NC data for annual analysis

#Set up a for loop to run through all files in dataset                
annualPath=wrkdir+'annual_anl/'
for dirName, subdirList, fileList in os.walk(wrkdir):
    for filename in fileList:
        if filename.endswith('.tif') or filename.endswith('.tiff'):      
            if "NC" in filename: #For both hourly and daily data
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
                        if int(date.year)==yearInt: #Compare file date with the year loop
                            shutil.copy2(fpath, annualPath+yearStr) #Copy the file to the appropriate directory
                    except:
                        pass
             
                
#Sort and copy NC data for simplified (JJA) seasonal analysis

#Set up a for loop to run through all files in dataset 
simpseasonalPath=wrkdir+'simpseasonal_anl/'                    
for dirName, subdirList, fileList in os.walk(wrkdir):
    for filename in fileList:
        if filename.endswith('.tif') or filename.endswith('.tiff'):       
            if "NC" in filename: #For both hourly and daily data
                fname = filename
                fpath = (dirName+'/'+fname) #Get file path for copying the file later
                fnameBase = os.path.splitext(filename)[0] #Remove the extension for more easier datetime extraction
                dateName = fnameBase[7:-4] #Extract the date portion of the file name string
                DB_TIME_FORMAT = '%Y%m%d%H' #Set up the formatting of the string date in the file name
                date = datetime.datetime.strptime(dateName, DB_TIME_FORMAT) #interpret the date time from the string
                try:
                    if 1==int(date.month) or 2==int(date.month) or 12==int(date.month):
                        shutil.copy2(fpath, simpseasonalPath+'/winter') #Copy the file to the appropriate directory
                    elif 3==int(date.month) or 4==int(date.month) or 5==int(date.month):
                        shutil.copy2(fpath, simpseasonalPath+'/spring')
                    elif 6==int(date.month) or 7==int(date.month) or 8==int(date.month):
                        shutil.copy2(fpath, simpseasonalPath+'/summer')
                    elif 9==int(date.month) or 10==int(date.month) or 11==int(date.month):
                        shutil.copy2(fpath, simpseasonalPath+'/fall')
                except:
                    pass
                    

#Sort and copy NC data for true calendar date seasonal analysis

"""
VERNAL EQUINOX.....(SPRING) MAR 19 or 20        (0320)
SUMMER SOLSTICE....(SUMMER) JUN 20 or 21 2019   (0621)
AUTUMNAL EQUINOX...(FALL) SEP 22 or 23 2019     (0922)
WINTER SOLSTICE....(WINTER) DEC 21 or 22 2019   (1221)
"""
#Set up a for loop to run through all files in dataset 
trueseasonalPath=wrkdir+'trueseasonal_anl/'                    
for dirName, subdirList, fileList in os.walk(wrkdir):
    for filename in fileList:
        if filename.endswith('.tif') or filename.endswith('.tiff'):       
            if "NC" in filename: #For both hourly and daily data
                fname = filename
                fpath = (dirName+'/'+fname) #Get file path for copying the file later
                fnameBase = os.path.splitext(filename)[0] #Remove the extension for more easier datetime extraction
                dateName = fnameBase[7:-4] #Extract the date portion of the file name string
                DB_TIME_FORMAT = '%Y%m%d%H' #Set up the formatting of the string date in the file name
                date = datetime.datetime.strptime(dateName, DB_TIME_FORMAT) #interpret the date time from the string
                dateComp = date.strftime('%m%d') 
                try:
                    if 101 <= int(dateComp) < 320:
                        shutil.copy2(fpath, trueseasonalPath+'/winter') #Copy the file to the appropriate directory
                    elif 1221 <= int(dateComp) <= 1231:
                        shutil.copy2(fpath, trueseasonalPath+'/winter')
                    elif 320 <= int(dateComp) < 621:
                        shutil.copy2(fpath, trueseasonalPath+'/spring')
                    elif 621 <= int(dateComp) < 922:
                        shutil.copy2(fpath, trueseasonalPath+'/summer')
                    elif 922 <= int(dateComp) < 1221:
                        shutil.copy2(fpath, trueseasonalPath+'/fall')
                except:
                    pass
                
#Sort and copy NC data for NLCD analysis
#IN PROGRESS
nlcdPath=wrkdir+'nlcd_anl/'                    
for dirName, subdirList, fileList in os.walk(wrkdir):
    for filename in fileList:
        if filename.endswith('.tif') or filename.endswith('.tiff'):       
            if "NC" in filename: #For both hourly and daily data
                fname = filename
                fpath = (dirName+'/'+fname) #Get file path for copying the file later
                fnameBase = os.path.splitext(filename)[0] #Remove the extension for more easier datetime extraction
                dateName = fnameBase[7:-4] #Extract the date portion of the file name string
                DB_TIME_FORMAT = '%Y%m%d%H' #Set up the formatting of the string date in the file name
                date = datetime.datetime.strptime(dateName, DB_TIME_FORMAT) #interpret the date time from the string
                try:
                    if 2001 <= int(date.year) < 2004:
                        shutil.copy2(fpath, nlcdPath+'/2001') #Copy the file to the appropriate directory
                    elif 2004 <= int(date.year) < 2006:
                        shutil.copy2(fpath, nlcdPath+'/2004')
                    elif 2006 <= int(date.year) < 2008:
                        shutil.copy2(fpath, nlcdPath+'/2006')
                    elif 2008 <= int(date.year) < 2011:
                        shutil.copy2(fpath, nlcdPath+'/2008')
                    elif 2011 <= int(date.year) < 2013:
                        shutil.copy2(fpath, nlcdPath+'/2011')
                    elif 2013 <= int(date.year) < 2016:
                        shutil.copy2(fpath, nlcdPath+'/2013')                        
                    elif 2016 <= int(date.year):
                        shutil.copy2(fpath, nlcdPath+'/2016')                        
                except:
                    pass

            
                
#Sort and copy NC data for SSC analysis
                
                #BEST WAY TO RUN THIS WILL BE USING GREP TO SEARCH THE TEXTFILE FOR THE DATE, READ THE SECOND COLUMN, THEN MOVE THE FILE BASED ON THAT VALUE INFORMATION
                #THAT OR I NEED TO FIND A BETTER WAY TO SEARCH A TEXT FILE WITHOUT HAVING TO REOPEN AND SCAN THE WHOLE THING
                #ALTHOUGH, THAT IS ALL GREP IS REALLY DOING ANYWAYS....

#Set up a for loop to run through all files in dataset 
sscPath = wrkdir+'ssc_anl/'

#Read in the SSC index file
inputfile = "C:/Users/zarzarc/OneDrive/Desktop/Research/WFU/surface-atmosphere/se-precip/data/ssc/gso_ssc.txt" 
infile = open(inputfile, 'r')
infileList = infile.readlines()
infile.close()

for dirName, subdirList, fileList in os.walk(wrkdir):
    for filename in fileList:
        if filename.endswith('.tif') or filename.endswith('.tiff'):
            if "NC" in filename: #For both hourly and daily data
                fname = filename
                fpath = (dirName+'/'+fname) #Get file path for copying the file later
                fnameBase = os.path.splitext(filename)[0] #Remove the extension for more easier datetime extraction
                dateName = fnameBase[7:-4] #Extract the date portion of the file name string
                DB_TIME_FORMAT = '%Y%m%d%H' #Set up the formatting of the string date in the file name
                date = datetime.datetime.strptime(dateName, DB_TIME_FORMAT) #interpret the date time from the string
                dateComp = date.strftime('%Y%m%d') 
                try: 
                    for line in infileList: 
                        sscDate = datetime.datetime.strptime(line[4:12], '%Y%m%d' ).strftime('%Y%m%d') #interpret the date time from the string
                        if dateComp == sscDate:
                            ssc = line[13]
                            if int(ssc)==1:
                                shutil.copy2(fpath, sscPath+'/dm')    
                            elif int(ssc) == 2:
                                shutil.copy2(fpath, sscPath+'/dp')   
                            elif int(ssc) == 3:
                                shutil.copy2(fpath, sscPath+'/dt')             
                            elif int(ssc) == 4:
                                shutil.copy2(fpath, sscPath+'/mm') 
                            elif int(ssc) == 5:
                                shutil.copy2(fpath, sscPath+'/mp') 
                            elif int(ssc) == 6:
                                shutil.copy2(fpath, sscPath+'/mt') 
                            elif int(ssc) == 7:
                                shutil.copy2(fpath, sscPath+'/t') 
                            elif int(ssc) == 8:
                                shutil.copy2(fpath, sscPath+'/miss')
                        
                except:
                    pass
            
      
            
## END ##