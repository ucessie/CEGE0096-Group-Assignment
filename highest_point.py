import rasterio
from shapely.geometry import Point
import geopandas as gpd
from rasterio import mask
import numpy as np
import json
from pyproj import CRS


class Clip:

    def buffer(x, y):
        # Store as point object
        # in km
        user_point = Point(x, y)
        # buffer a 5 km region
        region = user_point.buffer(5000)
        return region

    def square_buffer(self):
        geo = gpd.GeoDataFrame({'geometry': self}, index=[0])
        square = geo.envelope
        return square

    def geo(buffer):
        # save buffer region in geopandas
        geo = gpd.GeoDataFrame({'geometry': buffer}, index=[0])
        geo.crs = {'init': 'epsg:27700'}

        # Transform the buffer to same crs
        return geo

    def getFeatures(gdf):
        """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
        return [json.loads(gdf.to_json())['features'][0]['geometry']]

    def mask_ras(raster, buffer):
        out_img, out_transform = mask.mask(raster, shapes=buffer['geometry'], crop=True, nodata=-1)
        return out_img, out_transform

    def meta_update(self, buffer_image, buffer_region, affine):
        # self represent the original file meta data
        meta_data = self.meta.copy()
        epsg_code = int(buffer_region.crs['init'][5:])
        meta_data.update(
            {"driver": "GTiff", "height": buffer_image.shape[1], "width": buffer_image.shape[2], "transform": affine,
             "crs": CRS.from_epsg(epsg_code).to_proj4()})
        return meta_data

    def clip_ras(image, meta_data):
        output = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\elevation\output.tif'
        with rasterio.open(output, 'w', **meta_data) as dest:
            dest.write(image)

    def clip_square(self, meta_data):
        output = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\background\bk_output.tif'
        with rasterio.open(output, 'w', **meta_data) as dest:
            dest.write(self)

    def search_highest_point(image):
        raster = rasterio.open(image, 'r')
        height_array = raster.read()
        # find maximum value and return all
        max = None
        for line in height_array:
            max = line.max()

        # return a np array of row and column
        rc = np.transpose(np.nonzero(height_array == max))

        # return a list of highest point coord, but we only take the first one
        set = [raster.xy(row, col) for item, row, col in rc]
        return set[0], max

    def user_elevation(image, x, y):
        raster = rasterio.open(image, 'r')
        height_array = raster.read(1)
        row, col = raster.index(x, y)
        user_elev = height_array[row, col]
        return user_elev
