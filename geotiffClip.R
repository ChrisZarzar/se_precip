##---------------------------------##
## Author: Christopher Zarzar
## Created: 2-Jul-2019

##Purpose: Clip and mask geotiff to polygon shapefile extent.

##CREATED 2-jul-2019 CHRIS ZARZAR
##adapted from: https://rpubs.com/ricardo_ochoa/416711 & https://www.neonscience.org/dc-crop-extract-raster-data-r & https://www.earthdatascience.org/courses/earth-analytics/lidar-raster-data-r/crop-raster-data-in-r/
##---------------------------------##

list.of.packages <- c("rgdal", "ggplot2", "raster", "sf")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)

# load necessary packages
library(rgdal)  # for vector work; sp package should always load with rgdal. 
library (raster)
library(ggplot2)
library(sf)



## set up the working directory
setwd("C:/Users/chris/OneDrive/Desktop/Research/WFU/surface-atmosphere/se-precip/data/sample_mpe/20190405")

## load in the raster
raw.prcp <- raster("ST4.20190405.tiff")

## assign missing data value
NAvalue(raw.prcp) <- 9999

## load in the clipping shapefile
nc.buffer <- readOGR("C:/Users/chris/OneDrive/Desktop/Research/WFU/surface-atmosphere/se-precip/data/gis/nc-state-boundary/NC_Shapefile_hrap_PCS_Buffered.shp")

## assign the clip extent
clip.extent <- nc.buffer

## check the coordinate system of the raster data
crs(raw.prcp)

## check out the coordinate system of the clip extent sf and make sure the raster and clip extent crs match
crs(clip.extent)


## USE THIS IN FUTURE TO SET UP A CRS COMPARISON AND AUTOMATIC REPROJECTION TO HRAP GRID IF THEY DO NOT MATCH
## see here for more help with projections: https://www.earthdatascience.org/courses/earth-analytics/spatial-data-r/reproject-vector-data/
## proj.clip.extent <- 

## plot the data
plot(raw.prcp, main="US MPE Data")

plot(clip.extent, add=TRUE)

## more advanced plot and check the sf clip extent
#ggplot() +
  #geom_sf(data = proj.clip.extent, aes(fill=TYPE)) +
  #scale_color_manual(name = "Legend", values = nc.urban$TYPE) + ##CANNOT GET THE LEGEND TITLE TO WORK
  #ggtitle("NC Counties and Urban Areas") +
  #coord_sf()

## clear the plot when finished with it
## dev.off()

## crop the raster data down to the clip extent
crop.ras <- crop(raw.prcp, clip.extent)

## mask the cropped raster to limit the values used in analysis to those within the buffer.
final.ras <- mask(crop.ras, clip.extent)
  
## check that this worked by plotting the new data
plot(final.ras, main = "Cropped MPE Precip")
plot(clip.extent, add=TRUE)

## write out the final edited raster
writeRaster(final.ras, filename = "NC_ST4.20190405.tiff", overwrite = TRUE)



