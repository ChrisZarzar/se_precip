' Extract data from full precip files using linNums.prn file output from findLineNums.py program '

from numpy import *

lineNumFile = open ('lineNums.prn','rb')
lineNumArr = lineNumFile.readlines(); lineNumFile.close()

for year in range (2002,2003+1):
	yearShort = int(str(year)[2:])

	if (year >= 2004):
		area = 'US'
	else:
		area = 'LMRFC'

	for month in range (5,9+1):

		if (month==5 or month==7 or month==8):
			numDays = 31
		elif (month==6 or month==9):
			numDays = 30

		for day in range (1,numDays+1):
			print 'Working on %2.2d/%2.2d/%4.4d' % (month,day,year) 
			inputfile1 = '%4.4d/%s_prcp_%2.2d%2.2d%2.2d.dat' % (year,area,month,day,yearShort)
			try:
				infile1 = open (inputfile1,'rb')
				infileArr1 = infile1.readlines(); infile1.close()
			except:
				continue

			if (month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12):
				if day == 31:
					dayNew = 1
					monthNew = month + 1
				else:
					dayNew = day + 1
					monthNew = month
			elif (month==4 or month==6 or month==9 or month==11):
				if day == 30:
					dayNew = 1
					monthNew  = month + 1
				else:
					dayNew = day + 1
					monthNew = month
			elif (month==2):
				if (year%4 == 0):
					if day == 29:
						dayNew = 1
						monthNew = month + 1
					else:
						dayNew = day + 1
						monthNew = month
				else:
					if day == 28:
						dayNew = 1
						monthNew = month + 1
					else:
						dayNew = day + 1
						monthNew = month


			inputfile2 = '%4.4d/%s_prcp_%2.2d%2.2d%2.2d.dat' % (year,area,monthNew,dayNew,yearShort)
			try:
				infile2 = open (inputfile2,'rb')
				infileArr2 = infile2.readlines(); infile2.close()
			except:
				continue

			' Generate array to temporarily write data '
			assert len(infileArr1) == len(infileArr2), 'Input files 1 and 2 are not the same length...program aborted!'
			dataArr = ones((len(lineNumArr),26),'d')
			dataArr = dataArr * -999.

			' Use lineNumArr to find correct row of data, then write to array '
			for o in range (len(lineNumArr)):
				loc = int(lineNumArr[o])
				assert (float(infileArr1[loc][0:8]) == float(infileArr2[loc][0:8])), 'Data does not match...run findLineNums.py on current file.'
				dataArr[o,0] = float(infileArr1[loc][0:8])
				dataArr[o,1] = float(infileArr1[loc][8:16])
				for p in range (24):
					if (p < 19):
						dataArr[o,p+2] = float(infileArr1[loc][56+(p*8):64+(p*8)])
					else:
						dataArr[o,p+2] = float(infileArr2[loc][16+((p-19)*8):24+((p-19)*8)])

			' Write data to output file '
			outputfile = 'NoMS_prcp_%2.2d%2.2d%2.2d_LST.dat' % (month,day,yearShort)
			outfile = open (outputfile,'wb')
       
			for x in range (len(dataArr)):
				if (dataArr[x,0]<=-84. and dataArr[x,0]>=-95. and dataArr[x,1]>=29 and dataArr[x,1]<=38.):
					pass
				else:
					continue

				for y in range (len(dataArr[0])):
					if y == 0:
						outfile.write ('%.3f' % dataArr[x,y])
					else:
						outfile.write (',%.3f' % dataArr[x,y])                
				outfile.write ('\n')

			outfile.close()

