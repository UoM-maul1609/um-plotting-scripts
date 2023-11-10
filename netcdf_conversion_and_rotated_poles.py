import iris
#import matplotlib.pyplot as plt
#import iris.quickplot as qplt
import numpy as np
from iris.analysis.cartography import unrotate_pole
from netCDF4 import Dataset

ddir="/home/d01/msun/cylc-run/u-da799/share/cycle/20180811T1200Z/Regn123/resn_1/RAL3p2_504p4/um/"
fn="umnsaa_px.pp"
outfn=fn.replace('.pp','.nc')



data=iris.load(ddir+fn)
iris.save(data,outfn)
nc_file=Dataset(outfn,"a")


#lw_data=iris.load_cube(ddir+fn,iris.AttributeConstraint(STASH='m01s02i205'))

#print(lw_data.coord('grid_latitude').coord_system)

#pole_lat=39.2999 #or whatever you have
#pole_lon=179.5 #or whatever you have

pole_lat=nc_file['rotated_latitude_longitude'].grid_north_pole_latitude
pole_lon=nc_file['rotated_latitude_longitude'].grid_north_pole_longitude


rotated_lons=nc_file['grid_longitude'][:]   #sometimes this is grid_longitude in iris file....
rotated_lats=nc_file['grid_latitude'][:]

rlats=np.array([rotated_lats,]*len(rotated_lons)).transpose()
rlons=np.array([rotated_lons,]*len(rotated_lats))

#get real lats and lons
lons, lats = unrotate_pole(rlons, rlats, pole_lon, pole_lat)


lat=nc_file.createVariable('actual_latitude', np.float64, ('grid_latitude','grid_longitude',))
lon=nc_file.createVariable('actual_longitude', np.float64, ('grid_latitude','grid_longitude', ))
lat[:]=lats
lon[:]=lons

nc_file.close()

exit()

