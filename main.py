from user_input import IO






print("Enter the user location (as Easting and Northing)")

#Input user point
x, y = IO.user_input()
raster = IO.raster_input()

#Bounding box
print("Raster bounding box: ", raster.bounds)
print("Raster left bound: ", raster.bounds.left)
print("Raster right bound: ", raster.bounds.right)
print("Raster type: ", type(raster.bounds.left))
