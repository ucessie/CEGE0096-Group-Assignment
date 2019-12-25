from shapely.geometry import box
from shapely.geometry import Point
import geopandas as gpd
from rasterio import mask
import numpy as np
import json
import linecache
import codecs
import rasterio




class clip:

    def buffer(x, y):

        #Store as point object
        #in km
        user_point = Point(x,y)

        #buffer a 5 km region
        region = user_point.buffer(5000)

        return region

    def geo(buffer, elevation):

        #save buffer region in geopandas
        geo = gpd.GeoDataFrame({'geometry': buffer}, index=[0])
        geo.crs = {'init' :'epsg:27700'}

        #Transform the buffer to same crs
        return geo

    def getFeatures(gdf):
        """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
        return [json.loads(gdf.to_json())['features'][0]['geometry']]

    def mask_ras(raster, buffer):

        out_img, out_transform = mask.mask(raster, shapes= buffer['geometry'], crop=True)
        return out_img, out_transform
    def clip_ras(image, meta_data):

        out_tif = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\elevation\output.asc'
        with rasterio.open(out_tif, "w", **meta_data) as dest:
            dest.write(image)


    def load_asc(self):

        file = open(self, 'r', encoding = 'utf-8')
        region = np.loadtxt(file)

        #line1 = linecache.getline(r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\elevation\SZ.asc', 1)

        header = "ncols     %s\n" % region.shape[1]
        header += "nrows    %s\n" % region.shape[0]
        header += "xllcorner 425000.0\n"
        header += "yllcorner 75000.0\n"
        header += "cellsize 5.0\n"
        with open(region, 'w') as f:
            f.write(header)
            np.savetxt(self, region, header=header, fmt="%1.2f")
        return region
