import rasterio
import rasterio.plot
import pyproj
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class IO:

    def raster_input():

        #file input
        loadfile = ('/Users/joseph/Desktop/UCL/Geospatial programming/Material/background/raster-50k_2724246.tif')

        #load in rasterio
        geodata = rasterio.open(loadfile)


        return geodata


    def user_input():

                x = float(input("x coordinate: "))
                y = float(input("y coordinate: "))
                return x,y
