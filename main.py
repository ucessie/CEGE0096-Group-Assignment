from user_input import IO
from high_point import clip






print("Enter the user location (as Easting and Northing)")

#Input user point
x, y = IO.user_input()
raster = IO.raster_input()
elevation = IO.read_elevation()

'''
#Bounding box
print("Raster bounding box: ", raster.bounds)
print("Raster left bound: ", raster.bounds.left)
print("Raster right bound: ", raster.bounds.right)
print("Raster type: ", type(raster.bounds.left))
print(raster.crs)

#raster_output = IO.plot(raster,x,y)
print("Elevation Width and Height: ", elevation.width, elevation.height)
print("Elevation CRS: ", elevation.crs)
print("Elevation Boundary: ",elevation.bounds)
'''
#Takes buffer region
user_region = clip.buffer(x,y)
#Transform the buffer buffer region
region = clip.geo(user_region, elevation)
print(region.crs)
print("++++++++++++++++++++++++++++++++++++++++")
poly_area = region['geometry'].area
print(poly_area)

image, trans = clip.clip_ras(elevation, region)

#Plot Diagram
#plot_elevation = IO.plot(elevation)
