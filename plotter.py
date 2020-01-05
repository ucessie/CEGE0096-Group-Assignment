import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from rasterio.plot import show
import networkx as nx
from shapely.geometry import LineString
import geopandas as gpd
import numpy as np
import rasterio
import cartopy.crs as ccrs



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



    def draw_graph(graph, shortest_path, json_file):
        G = graph
        '''
        path_edges = zip(shortest_path, shortest_path[1:])
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_size=100, node_color='r')
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=10)
        nx.draw(G)
        '''

        roadlinks = json_file['roadlinks']
        links = []
        geom = []
        first_node = shortest_path[0]
        for node in shortest_path[1:]:
            link_fid = G.edges[first_node, node]['fid']
            links.append(link_fid)
            geom.append(LineString(roadlinks[link_fid]['coords']))
            first_node = node

        shortest_path_gpd = gpd.GeoDataFrame({"fid": links, "geometry": geom})
        return shortest_path_gpd

    def test(self, shortest_path_gpd):
        background = rasterio.open(str(self))
        back_array = background.read(1)
        palette = np.array([value for key, value in background.colormap(1).items()])
        background_image = palette[back_array]
        bounds = background.bounds
        extent = [bounds.left, bounds.right, bounds.bottom,  bounds.top]
        fig = plt.figure(figsize=(3, 3), dpi=300)
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.OSGB())

        ax.imshow(background_image, origin="upper", extent=extent, zorder=0)

        shortest_path_gpd.plot(ax=ax, edgecolor="blue", linewidth=0.5, zorder=2)




