from user_input import IO
from high_point import Clip
from ITN import ITN
from plotter import Plotter
from Shortest_path import Network

print("Enter the user location (as Easting and Northing)")
# indicate the initial file path
back_ground_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\background\raster-50k_2724246.tif'
background_region_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\background\bk_output.tif'
elevation_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\elevation\SZ.asc'
user_region_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\elevation\output.tif'
itn_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\itn\solent_itn.json'
# itn_file structure: TOID{[roadname];[links](start nodes ... end nodes)}
nodes_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\roads\nodes.shp'
links_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\roads\links.shp'
island_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\shape\isle_of_wight.shp'

print('Task 1 start here!!!!')
# Input user point
x, y = IO.user_input()
raster = IO.read_raster(back_ground_file)
elevation = IO.read_raster(elevation_file)
background = IO.read_raster(back_ground_file)
buffer_region = IO.read_raster(user_region_file)
background_region = IO.read_raster(background_region_file)
all_height = elevation.read(1)

print('------------------------------------------------------------\n')
print('Task 2 start here !!!!')
# Takes buffer region
user_region = Clip.buffer(x, y)
bk = Clip.square_buffer(user_region)
# Transform the buffer region
region = Clip.geo(user_region)
bk_region = Clip.geo(bk)

# access coordinate
coord = Clip.getFeatures(region)
bk_coord = Clip.getFeatures(bk_region)
# Check to see whether the area is correct
poly_area = bk_region['geometry'].area
print(poly_area)

# Create mask region using the buffer
# image is a numpy array
image, trans = Clip.mask_ras(elevation, region)
bk_image, bk_trans = Clip.mask_ras(background, bk_region)

# retrieve metadata and update the new buffer region
user_meta = Clip.meta_update(elevation, image, region, trans)
bk_meta = Clip.meta_update(background, bk_image, bk_region, bk_trans)

# execute clip method and return tif file
Clip.clip_ras(image, user_meta)
Clip.clip_square(bk_image, bk_meta)

# return highest point as tuple
hp_region = Clip.search_highest_point(user_region_file)

# access variables from buffer region file
print('----------------------------------------------------------\n')
print('Task 3 start here!!')
# read shape
road = ITN.read_json(itn_file)
node = ITN.read_shape(nodes_file)
links = ITN.read_shape(links_file)

start_node, end_node, start_x, start_y, end_x, end_y = ITN.load_tree(road, x, y, hp_region)
print('start point: ', (start_x, start_y))
print('user point: ', (x, y))
print('end point: ', (end_x, end_y))
print('highest_point: ', hp_region)
print(start_node)
print(end_node)

print('-------------------------------------------------------------\n')
print('Task 4 stat here!!!')
# Find shortest path
shortest_distance_path, G = Network.find_distance_shortest_path(road, start_node, end_node)
print('Shortest path (by distance weight): ', shortest_distance_path)

shortest_nais_path, G2 = Network.find_nais_rule_path(road, elevation, all_height, start_node, end_node)
print('Shortest path (by speed/time): ', shortest_nais_path)

print('-------------------------------------------------------------\n')
print('Task 5 stat here!!!')


# Plot Diagram
plot_simple = Plotter.draw_graph(G, shortest_distance_path, road)
plot_nais = Plotter.draw_graph(G2,shortest_nais_path, road)
test = Plotter.test(background_region_file, user_region_file, plot_simple, plot_nais,start_x, start_y, end_x, end_y, x, y, hp_region)

