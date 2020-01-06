import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from rasterio.plot import show
import networkx as nx
from shapely.geometry import LineString
import geopandas as gpd
import numpy as np
import rasterio
#import cartopy.crs as ccrs



class Plotter:


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

    def test(self, user_region, shortest_distance_path_gpd, shortest_nais_path_gpd, start_x, start_y, end_x, end_y, user_x, user_y, hp, handler):
        background = rasterio.open(str(self))
        background_image = background.read(1)
        user = rasterio.open(str(user_region))
        user_image = user.read(1)
        user_image[user_image == -1] = np.nan
        bounds = background.bounds
        extent = [bounds.left, bounds.right, bounds.bottom,  bounds.top]
        u_bound = user.bounds
        u_extent = [u_bound.left, u_bound.right, u_bound.bottom, u_bound.top]

        fig = plt.figure(figsize=(3, 3), dpi=300)
        ax = fig.add_subplot(1, 1, 1)

        if handler == 'shortest_path':
            plt.plot(user_x, user_y, 'bo', markersize=2, label='user location')
            plt.plot(hp[0], hp[1], 'go', markersize=2, label='highest point')
            plt.plot(start_x, start_y, 'b+', markersize=3, label='starting point')
            plt.plot(end_x, end_y, 'g+', markersize=3, label='ending point')
            st_x = [user_x, start_x]
            st_y = [user_y, start_y]
            ed_x = [end_x, hp[0]]
            ed_y = [end_y, hp[1]]
            plt.plot(st_x, st_y, 'b--', linewidth=1.0)
            plt.plot(ed_x, ed_y, 'g--', linewidth=1.0)
            shortest_nais_path_gpd.plot(ax=ax, edgecolor="red", linewidth=1.0, zorder=2, label='nais_path')
            shortest_distance_path_gpd.plot(ax=ax, edgecolor="black", linewidth=1.0, zorder=2, label='simple_path')

        elif handler == 'simple_point':
            plt.plot(user_x, user_y, 'ro', markersize=2, label='user point/highest point')

        elif handler == 'simple_path':
            plt.plot(user_x, user_y, 'bo', markersize=2, label='user location')
            plt.plot(hp[0], hp[1], 'go', markersize=2, label='highest point')
            st_x = [user_x, hp[0]]
            st_y = [user_y, hp[1]]
            plt.plot(st_x, st_y, 'b--', linewidth=1.0, label='simple path')

        ax.imshow(background_image, origin="upper", extent=extent, zorder=0)
        ax.imshow(user_image, origin="upper", extent=u_extent, alpha=0.6, zorder=1, vmin=0)
        plt.title('Flood Emergency Planning Map', fontsize=8)
        plt.axis('off')
        plt.legend(loc='best', fontsize=4, bbox_to_anchor=(0.5, 0, 0.5, 0.5))
        plt.show()

    def simple_point(self, background_file, user_file):
        background = rasterio.open(str(background_file))
        background_image = background.read(1)
        user = rasterio.open(str(user_file))
        user_image = user.read(1)
        user_image[user_image == -1] = np.nan
        bounds = background.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
        u_bound = user.bounds
        u_extent = [u_bound.left, u_bound.right, u_bound.bottom, u_bound.top]

        fig = plt.figure(figsize=(3, 3), dpi=300)
        ax = fig.add_subplot(1, 1, 1)
        plt.plot(self[0], self[1], 'ro', markersize=2, label='user point/highest point')


        plt.title('Flood Emergency Planning Map', fontsize=8)
        ax.imshow(background_image, origin="upper", extent=extent, zorder=0)
        ax.imshow(user_image, origin="upper", extent=u_extent, alpha=0.5, zorder=1)
        plt.axis('off')
        plt.legend(loc='best', fontsize=4, bbox_to_anchor=(0.5, 0, 0.5, 0.5))
        plt.show()

    def simple_path(self, user_x, user_y, background_file, user_file):
        background = rasterio.open(str(background_file))
        background_image = background.read(1)
        user = rasterio.open(str(user_file))
        user_image = user.read(1)
        user_image[user_image == -1] = np.nan
        bounds = background.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
        u_bound = user.bounds
        u_extent = [u_bound.left, u_bound.right, u_bound.bottom, u_bound.top]

        fig = plt.figure(figsize=(3, 3), dpi=300)
        ax = fig.add_subplot(1, 1, 1)
        plt.plot(self[0], self[1], 'ro', markersize=2, label='user point/highest point')
        st_x = [user_x, self[0]]
        st_y = [user_y, self[1]]
        plt.plot(st_x, st_y, 'b--', linewidth=1.0, label='simple path')
        plt.title('Flood Emergency Planning Map', fontsize=8)
        ax.imshow(background_image, origin="upper", extent=extent, zorder=0)
        ax.imshow(user_image, origin="upper", extent=u_extent, alpha=0.5, zorder=1)
        plt.axis('off')
        plt.legend(loc='best', fontsize=4, bbox_to_anchor=(0.5, 0, 0.5, 0.5))
        plt.show()




