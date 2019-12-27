from shapely.geometry import box
from shapely.geometry import Point
import geopandas as gpd
from rasterio import mask
import numpy as np
import json
import rasterio
from pyproj import CRS


class clip:

    def buffer(x, y):
        # Store as point object
        # in km
        user_point = Point(x, y)

        # buffer a 5 km region
        region = user_point.buffer(5000)

        return region

    def geo(buffer, elevation):
        # save buffer region in geopandas
        geo = gpd.GeoDataFrame({'geometry': buffer}, index=[0])
        geo.crs = {'init': 'epsg:27700'}

        # Transform the buffer to same crs
        return geo

    def getFeatures(gdf):
        """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
        return [json.loads(gdf.to_json())['features'][0]['geometry']]

    def mask_ras(raster, buffer):
        out_img, out_transform = mask.mask(raster, shapes=buffer['geometry'], crop=True)
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
        output = r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\elevation\output.asc'
        with rasterio.open(output, "w", **meta_data) as dest:
            dest.write(image)

    def load_asc(self):
        # convert to unicode

        file = open(self, 'r', encoding='utf-8')
        region = np.fromfile(file)

        # line1 = linecache.getline(r'C:\Users\Joseph\Desktop\UCL\Geospatial programming\Group Assignment\Material\elevation\SZ.asc', 1)

        header = "ncols     %s\n" % self.shape[1]
        header += "nrows    %s\n" % self.shape[0]
        header += "xllcorner 425000.0\n"
        header += "yllcorner 75000.0\n"
        header += "cellsize 5.0\n"
        with open(self, 'w', encoding='utf-8') as f:
            f.write(header)
            np.savetxt(self, region, header=header, fmt="%1.2f")
        return region
