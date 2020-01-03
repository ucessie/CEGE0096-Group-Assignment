import networkx as nx
from shapely.geometry import Point


class Network:

    def find_distance_shortest_path(self, start_node, end_node):
        # self=load json file in here
        G = nx.Graph()
        roadlinks = self['roadlinks']
        for link in roadlinks:
            G.add_edge(roadlinks[link]['start'],
                       roadlinks[link]['end'],
                       fid=link,
                       weight=roadlinks[link]['length'])
        edge = G.number_of_edges()
        node = G.number_of_nodes()

        path = nx.dijkstra_path(G, start_node, end_node, weight='weight')

        return path

    def find_nais_rule_path(self, elevation, height, start_node, end_node):
        # identify shortest path based on Naismith’s rule
        # 5km/hr and that an additional minute is added for every 10 meters of climb
        # speed = 5000/60 #meter/min
        #st_row, st_col = elevation.index(start_p.x, start_p.y)
        #en_row, en_col = elevation.index(end_p.x, end_p.y)
        #diff_elevation = height[en_row, en_col] - height[st_row, st_col]
        roadlinks = self['roadlinks']
        for link in roadlinks:
            start_p = Point(tuple(roadlinks[link]['coords'][0]))  # start of the road
            end_p = Point(tuple(roadlinks[link]['coords'][-1]))  # last element
            print(start_p, end_p, '\n')
