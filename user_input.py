import rasterio
import numpy as np

class Point:
    def __init__(self,id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def get_name(self):
        return self.id

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

class IO:


    def user_input():
        return 460000, 93000

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

    def read_raster(self):
        data = rasterio.open(self)
        return data


    def np_load_data(self):
        elevation = np.loadtxt(self)
        return elevation
