from user_input import IO
from high_point import Clip
from ITN import ITN
from plotter import Plotter
from Shortest_path import Network

print("Enter the user location (as Easting and Northing)")
# indicate the initial file path
back_ground_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\background\raster-50k_2724246.tif'
elevation_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\elevation\SZ.asc'
user_region_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\elevation\output.tif'
itn_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\itn\solent_itn.json'
# itn_file structure: TOID{[roadname];[links](start nodes ... end nodes)}
nodes_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\roads\nodes.shp'
links_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\roads\links.shp'
island_file = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\shape\isle_of_wight.shp'

# Input user point
x, y = IO.user_input()
raster = IO.raster_input(back_ground_file)
elevation = IO.read_elevation(elevation_file)
background = IO.load_background(back_ground_file)

# Takes buffer region
user_region = Clip.buffer(x, y)
# Transform the buffer buffer region
region = Clip.geo(user_region)

# access coordinate
coord = Clip.getFeatures(region)

# Check to see whether the area is correct
poly_area = region['geometry'].area
print(poly_area)

# Create mask region using the buffer
# image is a numpy array
image, trans = Clip.mask_ras(elevation, region)

# retrieve metadata and update the new buffer region
user_meta = Clip.meta_update(elevation, image, region, trans)

# execute clip method and return tif file
Clip.clip_ras(image, user_meta)

# return highest point as tuple
hp_region = Clip.search_highest_point(user_region_file)

# read shape
road = ITN.read_json(itn_file)
node = ITN.read_shape(nodes_file)
links = ITN.read_shape(links_file)

network, start_node, end_node, start_x, start_y, end_x, end_y = ITN.load_tree(road, x, y, hp_region)
print('start point: ', (start_x, start_y))
print('user point: ', (x, y))
print('end point: ', (end_x, end_y))
print('highest_point: ', hp_region)
print(start_node)
print(end_node)
print('Num of edge: ', network.number_of_edges())
print('Num of node: ', network.number_of_nodes())


# Find shortest path
shortest_path = Network.find_path(network, start_node, end_node)
print('Shortest path: ', shortest_path)

# Plot Diagram
#plot_all = Plotter.plotter(user_region_file,background,x,y,hp_region,start_x,start_y,end_x,end_y)
# plot_graph = Plotter.draw_graph(network, shortest_path)
