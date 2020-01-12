import rasterio
import numpy as np
from shapely.geometry import shape
import fiona
import shapely

class IO:

    def user_input(island):
        x_min = 430000
        x_max = 465000
        y_min = 80000
        y_max = 95000

        while True:
            try:
                x = float(input("x coordinate(between 430000 and 465000): "))
                y = float(input("y coordinate(between 80000, 95000): "))
                if x_min <= x <= x_max and y_min <= y <= y_max:
                    # Check if user is on the island
                    shp = fiona.open(island)
                    point = shapely.geometry.Point(x, y)
                    pol = shp.next()
                    geom = shape(pol['geometry'])
                    result = []
                    for poly in geom:
                        result.append(poly.contains(point))
                    if not any(result):
                        print('You are in the sea or out of the island!')
                    else:
                        return x, y
                else:
                    print("Out of Range!")
                    return IO.user_input(island)

            except ValueError:
                print("Wrong data type!")
                return IO.user_input(island)


    def read_raster(self):
        data = rasterio.open(self)
        return data

    def np_load_data(self):
        elevation = np.loadtxt(self)
        return elevation





