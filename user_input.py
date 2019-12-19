import rasterio
from rasterio.plot import show
from pyproj import Transformer
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import gdal

class IO:

    def raster_input():

        #file input
        loadfile = ('/Users/joseph/Desktop/UCL/Geospatial programming/Material/background/raster-50k_2724246.tif')

        #load in rasterio
        geodata = rasterio.open(loadfile)


        return geodata

    def plot(raster):


        show(raster, cmap='terrain')



    def user_input():

        x_min = 430000
        x_max = 465000
        y_min = 80000
        y_max = 95000

        while True:
            try:
                x = float(input("x coordinate: "))
                y = float(input("y coordinate: "))
                if x_min <= x <= x_max and y_min <= y <= y_max:
                    return x,y
                else:
                    print("Out of Range!")
                    return user_input()

            except ValueError:
                print("Wrong data tpye!")
                return user_input()



    def read_elevation():

        elevation = ('/Users/joseph/Desktop/UCL/Geospatial programming/Material/elevation/SZ.asc')
        data = rasterio.open(elevation)

        return data
