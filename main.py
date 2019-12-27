from user_input import IO
from high_point import clip

print("Enter the user location (as Easting and Northing)")
# indicate the initial file path
back_ground_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\background\raster-50k_2724246.tif'
elevation_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\elevation\SZ.asc'
user_region_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\elevation\output.asc'

# Input user point
x, y = IO.user_input()
raster = IO.raster_input(back_ground_file)
elevation = IO.read_elevation(elevation_file)


# Takes buffer region
user_region = clip.buffer(x, y)
# Transform the buffer buffer region
region = clip.geo(user_region, elevation)
print(region.crs)
region.head()
coord = clip.getFeatures(region)
print(coord)

print("++++++++++++++++++++++++++++++++++++++++")

# Check to see whether the area is correct
poly_area = region['geometry'].area
print(poly_area)

#Create mask region using the buffer
image, trans = clip.mask_ras(elevation, region)

print("++++++++++++++++++++++++++++++++++++++++")
# retrieve metadata and update the new buffer region
user_meta = clip.meta_update(elevation,image,region, trans)

# execute clip method and return ascii file
clip.clip_ras(image, user_meta)

# update the numpy array
hp_region = clip.load_asc(user_region_file)


#user_region = IO.read_user_region(user_region_file)

# read ascii data
#user_rg_np = IO.np_load_data(user_region_file)
#for line in user_region_file:
    #print(line)

# load asc data
#buffer_region = clip.load_asc(user_region_file)



# Plot Diagram
# plot_elevation = IO.plot(elevation)
#plot_buffer = IO.plot(user_region)
