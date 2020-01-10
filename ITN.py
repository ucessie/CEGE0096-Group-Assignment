from rtree import index
import geopandas as gpd
import json
import rasterio
from shapely.geometry import Point


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

    def load_tree(self, buffer_region ,user_x, user_y, highest_point):
        # GeoDataFrame of the shortest path
        # index for roadnodes with Rtree
        roadnodes = self['roadnodes']
        ids = list(roadnodes)
        # create a list of point object
        coord_lst = []
        idx = index.Index()
        for i, (fid, coords) in enumerate(roadnodes.items()):
            x, y = coords['coords']
            point = Point(x, y)
            if buffer_region.contains(point):
                idx.insert(i, [x, y, x, y], fid)

        # return the fid of the point
        start = list(idx.nearest((user_x, user_y, user_x, user_y), 1, objects=True))[0]
        end = list(idx.nearest((highest_point[0], highest_point[1], highest_point[0], highest_point[1]), 1, objects=True))[0]

        start_node = start.object
        end_node = end.object
        start_corr = start.bbox
        end_corr = end.bbox

        return start_node, end_node, start_corr[0], start_corr[1], end_corr[0], end_corr[1]
