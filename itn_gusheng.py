import json
from rtree import index
from shapely.geometry import Point

# Integrated Transport Network

class ITN:

    def __init__(self, user_point, highest_point):
        self.user_point = user_point
        self.highest_point = highest_point

    def get_itn(self):
        filepath = input("Please enter the filepath of the ITN file:\n")
        with open(filepath, "r") as f:
            itn = json.load(f)
        return itn

    def nearest_node(self):
        nodes = self.get_itn()["roadnodes"]
        ids = list(nodes)
        idx = index.Index()
        i = 0
        for node in nodes:
            idx.insert(i, nodes[node]["coords"])
            i += 1
        start_index = list(idx.nearest((self.user_point.x, self.user_point.y),
                                        1))
        end_index = list(idx.nearest((self.highest_point.x,
                                      self.highest_point.y), 2))
        start_node = ids[start_index[0]]
        end_node = ids[end_index[0]]
        start_coords = nodes[start_node]
        end_coords = nodes[end_node]
        return [start_node, start_coords, end_node, end_coords]

# test
itn = ITN(Point(450000, 90000), Point(447702.5, 85562.5))
print(itn.nearest_node())