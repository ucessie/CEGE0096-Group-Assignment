from user_input import IO
from high_point import clip
from ITN import ITN

print("Enter the user location (as Easting and Northing)")
# indicate the initial file path
back_ground_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\background\raster-50k_2724246.tif'
elevation_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\elevation\SZ.asc'
user_region_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\elevation\output.tif'
itn_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\itn\solent_itn.json'
#itn_file structure: TOID{[roadname];[links](start nodes ... end nodes)}
nodes_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\roads\nodes.shp'
links_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\roads\links.shp'
island_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\shape\isle_of_wight.shp'


# Input user point
x, y = IO.user_input()
raster = IO.raster_input(back_ground_file)
elevation = IO.read_elevation(elevation_file)
background = IO.load_background(back_ground_file)


# Takes buffer region
user_region = clip.buffer(x, y)
# Transform the buffer buffer region
region = clip.geo(user_region)

# access coordinate
coord = clip.getFeatures(region)


# Check to see whether the area is correct
poly_area = region['geometry'].area
print(poly_area)

#Create mask region using the buffer
#image is a numpy array
image, trans = clip.mask_ras(elevation, region)


# retrieve metadata and update the new buffer region
user_meta = clip.meta_update(elevation,image,region, trans)

# execute clip method and return tif file
clip.clip_ras(image, user_meta)

# return highest point as tuple
hp_region = clip.search_highest_point(user_region_file)


#read shape
road = ITN.read_json(itn_file)
node = ITN.read_shape(nodes_file)
links = ITN.read_shape(links_file)
for key in road.keys():
    print(key,road[key])
    print('\n')


# Plot Diagram
#plot_all = IO.plotter(image,background,x,y,hp_region)
