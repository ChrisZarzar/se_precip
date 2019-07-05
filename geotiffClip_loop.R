##---------------------------------##
## Author: Christopher Zarzar
## Created: 2-Jul-2019

##Purpose: Clip and mask folder of geotiffs to polygon shapefile extent.

##CREATED 2-jul-2019 CHRIS ZARZAR
##adapted from: https://rpubs.com/ricardo_ochoa/416711 & geotiffClip.R & Z_LPRClass_CIplotsV4.R
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
setwd("C:/Users/zarzarc/OneDrive/Desktop/Research/WFU/surface-atmosphere/se-precip/data/sample_mpe/20190405")

## set up other required mpe data and GIS directories
mainDir <- "C:/Users/zarzarc/OneDrive/Desktop/Research/WFU/surface-atmosphere/se-precip/data/"

mpeDir <- (paste(mainDir,"sample_mpe/20190405/",sep=''))

gisDir <- (paste(mainDir,"gis/nc-state-boundary/",sep='')) 


## load in the clipping vector
sf.clip <- paste(gisDir,"NC_Shapefile_hrap_PCS_Buffered.shp",sep='')
nc.buffer <- readOGR(sf.clip)

## assign the clip extent
clip.extent <- nc.buffer

## loop set up to work through directory of tiffs
file.cmd <- paste('files <- file.info(list.files(path=mpeDir, pattern="*.tiff", full.names = TRUE, recursive = FALSE))', sep='')
eval(parse(text=file.cmd))
fileList <- rownames(files)

for (currentFile in fileList){
  fileBase = basename(currentFile)
  fileOut = paste(mpeDir,"NC_",fileBase,sep='')
  
  ## load in the raster
  raw.prcp <- raster(currentFile)
  
  ## assign missing data value mainly for plotting purposes
  NAvalue(raw.prcp) <- 9999
  
  ## crop the raster data down to the clip extent
  crop.ras <- crop(raw.prcp, clip.extent)
  
  ## mask the cropped raster to limit the values used in analysis to those within the buffer.
  final.ras <- mask(crop.ras, clip.extent)
  
  ## reassign the missing values to 9999 avoid numpy Runtime warnings
  final.ras[is.na(final.ras)] <- 9999
  
  ## write out the final edited raster
  writeRaster(final.ras, filename = fileOut, overwrite = TRUE)
}


