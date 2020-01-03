import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from rasterio.plot import show
import networkx as nx


class Plotter:

    def plotter(buffer_region, background, user_x, user_y, high_point, sx, sy, ex, ey):
        left = float(background.bounds.left)
        right = float(background.bounds.right)
        bottom = float(background.bounds.bottom)
        top = float(background.bounds.top)
        # Plot on a map
        plt.scatter(high_point[0], high_point[1], c='r')
        plt.scatter(user_x, user_y, c='b')
        plt.scatter(sx, sy)
        plt.scatter(ex, ey, c='g')
        #show(buffer_region, bounds= True, cmap='terrain')
        # img = mpimg.imread(buffer_region)
        # plt.imshow(img, cmap='terrain',alpha=0.5, z)
        # plt.legend()
        # plt.imshow(background, extent=[left, right, bottom, top])
        plt.show()



    def draw_graph(self, shortest_path):
        G = self
        path_edges = zip(shortest_path, shortest_path[1:])
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_size=100, node_color='r')
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=10)
        plt.show()
        nx.draw(G)
        plt.show()
