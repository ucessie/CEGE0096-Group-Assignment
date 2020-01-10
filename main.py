from user_input import IO
from highest_point import Clip
from ITN import ITN
from plotter import Plotter
from Shortest_path import Network
from functools import reduce
import test_os
import os

# path to main.py
file_os = test_os.get_my_path()
# go 2 directory levels up
material_path = reduce(lambda x, f: f(x), [os.path.dirname] * 2, file_os)
back_ground_file = str(os.path.join(material_path, 'Material', 'background', 'raster-50k_2724246.tif'))
elevation_file = str(os.path.join(material_path, 'Material', 'elevation', 'SZ.asc'))
itn_file = str(os.path.join(material_path, 'Material', 'itn', 'solent_itn.json'))
nodes_file = str(os.path.join(material_path, 'Material', 'roads', 'nodes.shp'))
links_file = str(os.path.join(material_path, 'Material', 'roads', 'links.shp'))
island_file = str(os.path.join(material_path, 'Material', 'shape', 'isle_of_wight.shp'))

# indicate the initial file path
print('Task 1 start here!!!!')
print("Enter the user location (as Easting and Northing):")
# Input user point
x, y = IO.user_input(island_file)
raster = IO.read_raster(back_ground_file)
elevation = IO.read_raster(elevation_file)
background = IO.read_raster(back_ground_file)
all_height = elevation.read(1)
# read shape
road = ITN.read_json(itn_file)
node = ITN.read_shape(nodes_file)
links = ITN.read_shape(links_file)

user_elev = Clip.user_elevation(elevation_file, x, y)
print('User elevation: ', user_elev)

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

# Create mask region using the buffer
# image is a numpy array
image, trans = Clip.mask_ras(elevation, region)
bk_image, bk_trans = Clip.mask_ras(background, bk_region)

# retrieve metadata and update the new buffer region
user_meta = Clip.meta_update(elevation, image, region, trans)
bk_meta = Clip.meta_update(background, bk_image, bk_region, bk_trans)

# execute clip method, return tif file and assign new output file here
Clip.clip_ras(image, user_meta, material_path)
Clip.clip_square(bk_image, bk_meta, material_path)
background_region_file = str(os.path.join(material_path, 'Material', 'background', 'bk_output.tif'))
user_region_file = str(os.path.join(material_path, 'Material', 'elevation', 'output.tif'))

# return highest point as tuple
hp_region, height_max = Clip.search_highest_point(user_region_file)
print('Highest point elevation: ', height_max)

# case where user point is highest point
if hp_region == (x, y) or height_max == user_elev:
    print('You are very safe!!')
    test = Plotter.test(background_region_file, back_ground_file, user_region_file, 0, 0, 0, 0, 0, 0, x, y, hp_region, 'simple_point')
else:
    # access variables from buffer region file
    print('----------------------------------------------------------\n')
    print('Task 3 start here!!')

    start_node, end_node, start_x, start_y, end_x, end_y = ITN.load_tree(road, user_region, x, y, hp_region)
    print('start point: ', (start_x, start_y))
    print('user point: ', (x, y))
    print('end point: ', (end_x, end_y))
    print('highest_point: ', hp_region)
    print('start node(FID): ', start_node)
    print('end node(FID):', end_node)

    print('-------------------------------------------------------------\n')
    print('Task 4 start here!!!')
    # Find shortest path
    shortest_distance_path, G = Network.find_distance_shortest_path(road, start_node, end_node)
    print('Shortest path (by distance weight): ', shortest_distance_path)

    shortest_nais_path, G2 = Network.find_nais_rule_path(road, elevation, all_height, start_node, end_node)
    print('Shortest path (by speed/time): ', shortest_nais_path)

    print('-------------------------------------------------------------\n')
    print('Task 5 start here!!!')


    # Plot Diagram
    plot_simple = Plotter.draw_graph(G, shortest_distance_path, road)
    plot_nais = Plotter.draw_graph(G2,shortest_nais_path, road)
    test = Plotter.test(background_region_file, back_ground_file, user_region_file, plot_simple, plot_nais, start_x, start_y, end_x, end_y, x, y, hp_region, 'shortest_path')

