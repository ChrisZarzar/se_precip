## load the raster, sp, and rgdal packages
library(raster)
library(gdal)
library(sf)
library(ggplot2)

raw.nlcd <- raster('C:/Users/zarzarc/OneDrive/Desktop/Research/WFU/surface-atmosphere/urban-precip/[FILE]')

## load in the state shapefile
nc.counties <- st_read("gis/CountyBoundary/BoundaryCountyPolygon.shp")

## load in the urban boundaries shapefile
nc.urban <- st_read("gis/Smooth_Urban_Boundary/SmoothedUrbanBoundary.shp")

## let the clip extent
clip.extent <- nc.counties

## check out the coordinate system of the clip extent sf
st_crs(clip.extent)

## check the coordinate system of the nlcd data
crs(raw.nlcd)

## project the coordinate system data to the nlcd data to ensure the clip will function properly
## see here for more help with projections: https://www.earthdatascience.org/courses/earth-analytics/spatial-data-r/reproject-vector-data/
proj.clip.extent <- 


## plot and check the sf clip extent
ggplot() +
  geom_sf(data = proj.clip.extent, aes(fill=TYPE)) +
  scale_color_manual(name = "Legend", values = nc.urban$TYPE) + ##CANNOT GET THE LEGEND TITLE TO WORK
  ggtitle("NC Counties and Urban Areas") +
  coord_sf()

## clear the plot when finished with it
dev.off()

## crop the nlcd data down to the clip extent
crop.nlcd <- crop(raw.nlcd, clip.extent)

## check that this worked by plotting the new data
plot(lidar_chm_crop, main = "Cropped NLCD")

