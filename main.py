from user_input import IO
from high_point import clip
import pycrs

print("Enter the user location (as Easting and Northing)")
# indicate the initial file path
back_ground_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\background\raster-50k_2724246.tif'
elevation_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\elevation\SZ.asc'
user_region_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\elevation\output.asc'

# Input user point
x, y = IO.user_input()
raster = IO.raster_input(back_ground_file)
elevation = IO.read_elevation(elevation_file)



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
# Takes buffer region
user_region = clip.buffer(x, y)
# Transform the buffer buffer region
region = clip.geo(user_region, elevation)
print(region.crs)

coord = clip.getFeatures(region)
print(coord)

print("++++++++++++++++++++++++++++++++++++++++")

# Check to see whether the area is correct
poly_area = region['geometry'].area
print(poly_area)

#Create mask region using the buffer
image, trans = clip.mask_ras(elevation, region)

print(type(image)) #numpy ndarray
print(type(trans)) #affine


# retrieve metadata
meta_data = elevation.meta.copy()
print(meta_data)

# retrieve coordinate reference
epsg_code = int(region.crs['init'][5:])
print("espg code:", epsg_code)

print("++++++++++++++++++++++++++++++++++++++++")

meta_data.update({"driver": "GTiff", "height": image.shape[1], "width": image.shape[2], "transform": trans,
                  "crs": pycrs.parse.from_epsg_code(epsg_code).to_proj4()})

# execute clip method and return tif file
clip.clip_ras(image, meta_data)
user_region = IO.read_user_region(user_region_file)

# load asc data
#buffer_region = clip.load_asc(user_region_file)



# Plot Diagram
# plot_elevation = IO.plot(elevation)
plot_buffer = IO.plot(user_region)
