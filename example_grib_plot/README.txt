The attached zipped file has a sample program and 24 hourly GRIB files to get you started.  It is much easier to plot the GRIB files using matplotlib and Basemap since the geographic data are still intact.  The processed data files are easier to work with in calculations, but can be more easily plotted in a GIS program.

As for the findLineNum.py script, yes I generated the compare.prn file manually.  The easiest way to do that is by cropping the HRAP grid points you need from a polygon (i.e., states shapefile).  As for the assumption I made about the order of the files (sometimes I laugh at my own documentation), you are correct that this just means the lat and lon should remain in the same order.  I wrote this script quite quickly (obviously), so that is an easy workaround if needed.

