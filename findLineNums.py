' Find line numbers for specific latlon locations using the compare.prn file '

from numpy import *

compareFile = open ('compare.prn','rb')
compareArr = compareFile.readlines(); compareFile.close()

inputfile = raw_input ('Input filename: ')
infile = open (inputfile,'rb')
infileArr = infile.readlines(); infile.close()

outfile = open ('lineNums.prn','wb')

' Generate list of latlons in input file...assume that the order of input files 1 and 2 are the same (gulp) '
locList = list()
for i in range (len(infileArr)):
	locStr = '%8.3f%8.3f' % (float(infileArr[i][0:8]), float(infileArr[i][8:16]))
	locList.append(locStr)

' Use index function to find correct row of data, then write to array '
for o in range (len(compareArr)):
	loc = locList.index(str(compareArr[o][0:16]))
	outfile.write ('%d\n' % loc)

outfile.close()

