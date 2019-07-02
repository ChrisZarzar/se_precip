#! /usr/bin/ python
# coding=utf-8
"""
Purpose: This script will process the GRIB MPE data supplied from Dr. Jamie Dyer.


"""
__version__ = "$Revision: 1.0 $"[11:-2]  # type: str
__date__ = "$Date: 2019/06/27 18:38:47 $"[7:-2]
__author__ = "Chris Zarzar <chriszarzar@gmail.com>"

"""
Author: Chris Zarzar
Notes: In the mpe_data_explore.py script I process and explore teh CSV data because it makes it easy to pull out
quick numbers. In this script, I will be subsetting, processing, plotting, and running raster calcualtions
on the MPE grib data supplied by Dr. Dyer. 
    
Requirements:
1. Numpy
2. Pygrib
3. raster
4. gdal
5. sf
6. ggplot2
7. matplotlib

________________________________________________________
#### HISTORY ####

27-jun-2019 [Chris Zarzar]: Created. . 


______________________________________________________________________________
"""
