install.packages("raster")
install.packages("rgdal")
install.packages("FedData")
install.packages("ggplot2")

## load the raster, sp, and rgdal packages
library(raster)
library(sp)
library(sf)
library(rgdal)
library(FedData)
library(ggplot2)

## set working directory to data folder
setwd("C:/Users/zarzarc/OneDrive/Desktop/Research/WFU/surface-atmosphere/urban-precip/")

## load in the state shapefile
nc.counties <- st_read("data/gis/CountyBoundary/BoundaryCountyPolygon.shp")

## load in the urban boundaries shapefile
nc.urban <- st_read("data/gis/Smooth_Urban_Boundary/SmoothedUrbanBoundary.shp")

## plot the state shapefile
ggplot() +
  geom_sf(data = nc.counties, size = 1.5, color = "black", fill = "NA") +
  geom_sf(data = nc.urban, size = 0.5, color = "gray", fill = "brown") +
  ggtitle("NC Counties and Urban Areas") +
  coord_sf()



# load raster in R object called 'DEM"
DEM <-raster("NEON-DS-Field-Site-spatial-Data/SJER/DigitalTerrainModel/SJER2013_DTM.tif")
# Get min and max cell values from raster
#NOTE: this code may fail if the raster is too large
cellStats(DEM, min)
cellStats(DEM, max)
cellStats(DEM, range)
#view coordinate reference system
DEM@crs
## CRS arguments:
## +proj=utm +zone=11 +datum+WGS84 +units=m +no_defs +ellps+WGS84
## +towgs84= O,O,O
# the distribution of the values in the raster
hist(DEM, main="Distribution of elevation values", col="purple", maxpixels=22000000)
# plot the raster
# note that this raster repsresents a small region of the NEON SJER field site
plot (DEM, main= "Digital Elevation Model, SJER") #add title with main
# create a plot of our raster
image (DEM)
#specify the range of values that you want to plot in the DEM
# just plot pixels between 250 and 300 m in elevation
image(DEM, zlim=c(250,300))
# we can specify the colors too
col <- terrain.colors(5)
image(DEM, zlim=c(250,375), main="Digital Elevation Model (DEM)", col=col)
# add a color map with 5 colors
col=terrain.colors(5)

# add breaks to the colormap (6 breaks = 5 segments)
brk <- c(250, 300, 350, 400, 450, 500)
plot(DEM, col=col, breaks=brk, main="DEM with more breaks")
# First, expand right side of clipping rectangle to make room for the legend
# turn xpd off
par(xpd = FALSE, mar=c(5.1, 4.1, 4.1, 4.5))
# Second, plot w/ no legend
plot(DEM, col=col, breaks=brk, main="DEM with a Custom (but flipped) Legend", legend = FALSE)
# Third, turn xpd back on to force the legend to fit next to the plot 
par(xpd = TRUE)
# Fourth, add a legend - & make it appear outside of the plot 
legend(par()$usr[2], 4110600, legend =c("lowest", "a bit higher", "middle ground", "higher yet", "highest"), fill = col)
# Exapnd right side of clipping rect to make room for tge legend
par(xpd = FALSE, mar=c(5.1, 4.1, 4.1, 4.5))
#DEM with a custom legend
plot(DEM, col=col, breaks=brk, main="DEM with a Custom Legend",legend = FALSE)
#turn xpd back on to force the legend to fit next to the plot.
par(xpd = TRUE)
#add a legend - but make it appear outside of the plot
legend( par()$usr[2], 4110600,
        legend = c("Highest", "Higher yet", "Middle","A bit higher", "Lowest"), 
        fill = rev(col))
#add a color map with 4 colors
col=terrain.colors(4)
#add breaks to the colormap (6 breaks = 5 segments)
brk,<- c(200, 300, 350, 400,500)
plot(DEM, col=col, breaks=brk, main="DEM with fewer breaks")
#multiple each pixel in the raster by 2
DEM2 <- DEM * 2
DEM2
#plot the new DEM
plot(DEM2, main="DEM with all values doubled")
#plot the DEM
plot(DEM)
# Define  the extent of the crop by clicking on the plot
cropbox1 <- drawExtent ()
#crop the raster, then plot the new cropped raster
DEMcropl <- crop(DEM, cropbox1)
#plot the cropped extent
plot(DEMcropl)
#define the crop extent
cropbox2 <- c(255077.3,257158.6,4109614,4110934)
#crop the raster
DEMcrop2 <- crop(DEM, cropbox2)
#plot cropped DEM
plot(DEMcrop2)
##end
