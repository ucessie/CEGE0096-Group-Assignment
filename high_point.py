from shapely.geometry import box
from shapely.geometry import Point
import geopandas as gpd
from rasterio import mask
import json




class clip:

    def buffer(x, y):

        #Store as point object
        #in km
        user_point = Point(x,y)

        #buffer a 5 km region
        region = user_point.buffer(5)

        return region

    def geo(buffer, elevation):

        #save buffer region in geopandas
        geo = gpd.GeoDataFrame({'geometry': buffer}, index=[0])
        geo.crs = {'init' :'epsg:27700'}

        #Transform the buffer to same crs
        return geo

    def clip_ras(raster, buffer):

        out_img, out_transform = mask.mask(raster, shapes= buffer['geometry'], crop=True)
        return out_img, out_transform
