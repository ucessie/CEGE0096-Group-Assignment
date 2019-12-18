import rasterio
import rasterio.plot
import pyproj
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class input():
    def __init__(self,):





    def input():

        #file input
        print('Load File')
        loadfile = ('/Users/joseph/Desktop/UCL/Geospatial programming/Material/background/raster-50k_2724246.tif')

        #load in rasterio
        geodata = rasterio.open(loadfile)

        #Bounding box
        print("Raster bounding box: ", geodata.bounds)
        print("Raster left bound: ", geodata.bound.left)
        print("Raster right bound: ", geodata.bound.right)
        print("Raster type: ", type(geodata.bounds))
