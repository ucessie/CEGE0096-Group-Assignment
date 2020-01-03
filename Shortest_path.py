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
        # G2 for naismith rule
        G2 = nx.Graph()
        speed = float(5000 / 60)  # meter/min
        roadlinks = self['roadlinks']

        # start of the road

        for link in roadlinks[1:]:
            count = 1
            ele_time = 0
            start_p = Point(tuple(roadlinks[link]['coords'][0]))
            for point in link:
                end_p = Point(tuple([point]['coords'][count]))  # last element
                st_row, st_col = elevation.index(start_p.x, start_p.y)
                en_row, en_col = elevation.index(end_p.x, end_p.y)
                diff_elevation = height[int(en_row), int(en_col)] - height[int(st_row), int(st_col)]
                ele_time = float(diff_elevation / 10)
                count = count + 1
                start_p = end_p
            time = ele_time + roadlinks[link]['length'] / speed

            G2.add_edge(roadlinks[link]['start'],
                        roadlinks[link]['end'],
                        fid=link,
                        weight=time)


        nais_path = nx.dijkstra_path(G2, source=start_node, target=end_node, weight="weight")
        return nais_path
