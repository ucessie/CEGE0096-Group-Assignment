import matplotlib
import matplotlib.pyplot as plt
from rasterio.plot import show


class Plotter:

    def plotter(buffer_region, background, user_x, user_y, high_point, sx,sy,ex,ey):
        # Plot on a map
        plt.scatter(high_point[0], high_point[1], c='r')
        plt.scatter(user_x, user_y, c='b')
        plt.scatter(sx,sy)
        plt.scatter(ex,ey, c='g')
        #plt.legend()
        # plt.imshow(background.read(1))
        #plt.imshow(buffer_region, cmap='terrain')
        plt.show()

        # show(raster, cmap='terrain')
