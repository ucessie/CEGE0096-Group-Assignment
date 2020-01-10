from rtree import index
import geopandas as gpd
import json
from user_input import Point
import rasterio


class ITN:

    def read_elevation(self):
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
            coord_lst.append(Point(i, x, y))
            i += 1

        for pt in coord_lst:
            idx.insert(id, (pt.get_x(), pt.get_y(), pt.get_x(), pt.get_y()))
            id += 1

        # return the id of the point
        start_index = list(idx.nearest((user_x, user_y), 1))[0]
        end_index = list(idx.nearest((highest_point[0], highest_point[1]), 1))[0]

        # return the coordinate of the nearest point
        start_corr = coord_lst[start_index]
        end_corr = coord_lst[end_index]

        # return the index of the node
        start_node = ids[start_index]
        end_node = ids[end_index]

        return start_node, end_node, start_corr.get_x(), start_corr.get_y(), end_corr.get_x(), end_corr.get_y()
