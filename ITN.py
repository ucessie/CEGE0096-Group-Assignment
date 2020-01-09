from rtree import index
import geopandas as gpd
import json
import rasterio
from shapely.geometry import Point

class ITN:

    def read_elevaton(self):
        raster = rasterio.open(self, 'r')
        height_array = raster.read()
        return height_array

    def read_shape(self):

        shape = gpd.read_file(self)
        return shape

    def read_json(self):
        # read file
        with open(self, 'r') as js:
            data = json.load(js)
            return data

    def load_tree(self, user_x, user_y, highest_point):
        # GeoDataFrame of the shortest path
        # index for roadnodes with Rtree
        roadnodes = self['roadnodes']

        ids = list(roadnodes)
        # create a list of point object
        coord_lst = []
        idx = index.Index()
        i = 0
        id = 1
        for node in roadnodes:
            x = roadnodes[node]['coords'][0]
            y = roadnodes[node]['coords'][1]
            coord_lst.append(Point(x, y))
            i += 1

        for pt in coord_lst:
            idx.insert(id, (pt.x, pt.y, pt.x, pt.y))
            id += 1

        # return the id of the point
        start_index = list(idx.nearest((user_x, user_y, user_x, user_y), 1))[0]
        end_index = list(idx.nearest((highest_point[0], highest_point[1], highest_point[0], highest_point[1]), 1))[0]

        # return the coordinate of the nearest point
        start_corr = coord_lst[start_index]
        end_corr = coord_lst[end_index]

        # return the index of the node
        start_node = ids[start_index]
        end_node = ids[end_index]

        return start_node, end_node, start_corr.x, start_corr.y, end_corr.x, end_corr.y
