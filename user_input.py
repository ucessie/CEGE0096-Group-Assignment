import rasterio
from rasterio.plot import show
from pyproj import Transformer
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from rasterio import crs
from rasterio import warp
import geopandas as gpd


class IO:

    def raster_input(self):
        # load in rasterio
        geodata = rasterio.open(self)

        return geodata

    def plotter(buffer_region, background, user_x, user_y, high_point):
        # Plot on a map
        plt.scatter(high_point[0], high_point[1], c='r')
        plt.scatter(user_x, user_y, c='b')
        #plt.imshow(background.read(1))
        plt.imshow(buffer_region, cmap='terrain')
        plt.show()

        # show(raster, cmap='terrain')

    def user_input():
        return 440000, 85000

        '''
        x_min = 430000
        x_max = 465000
        y_min = 80000
        y_max = 95000

        while True:
            try:
                x = float(input("x coordinate: "))
                y = float(input("y coordinate: "))
                if x_min <= x <= x_max and y_min <= y <= y_max:
                    return x, y
                else:
                    print("Out of Range!")
                    return user_input()

            except ValueError:
                print("Wrong data tpye!")
                return user_input()
        '''

    def read_elevation(self):
        data = rasterio.open(self)

        return data

    def read_user_region(self):
        image = rasterio.open(self)
        return image

    def np_load_data(self):
        elevation = np.loadtxt(self)
        return elevation

    def load_background(self):
        background = rasterio.open(self)
        #background, affine = warp.reproject(background, background, dst_crs = crs.CRS.from_epsg(27700) )
        return background
