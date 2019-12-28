from rtree import index
import geopandas as gpd
import json

class ITN:

    def read_shape(self):

        shape = gpd.read_file(self)
        return shape

    def read_json(self):
        # read file
        with open(self, 'r') as myfile:
            file = myfile.read()
            data = json.loads(file)

            return data
