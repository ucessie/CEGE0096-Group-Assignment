import networkx as nx
import rtree


class Network:

    def find_path(self, start_node, end_node):
        G = self
        path = nx.dijkstra_path(G, start_node, end_node)

        return path
