import iris
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import numpy as np
from iris.analysis.cartography import unrotate_pole

ddir="/home/d01/msun/cylc-run/u-da799/share/cycle/20180811T1200Z/Regn123/resn_1/RAL3p2_504p4/um/"
fn="umnsaa_px.pp"
outfn='test.nc'

data=iris.load(ddir+fn)
iris.save(data,outfn)



lw_data=iris.load_cube(ddir+fn,iris.AttributeConstraint(STASH='m01s02i205'))

print(lw_data.coord('grid_latitude').coord_system)

pole_lat=39.2999 #or whatever you have
pole_lon=179.5 #or whatever you have


rotated_lons=lw_data.coord('grid_longitude').points   #sometimes this is grid_longitude in iris file....
rotated_lats=lw_data.coord('grid_latitude').points

rlats=np.array([rotated_lats,]*len(rotated_lons)).transpose()
rlons=np.array([rotated_lons,]*len(rotated_lats))

#get real lats and lons
lons, lats = unrotate_pole(rlons, rlats, pole_lon, pole_lat)



plt.figure()
plt.pcolormesh(lons,lats,lw_data.data[11,:,:],shading='gouraud')
#plt.gca().coastlines()
#plt.show()

plt.savefig('./myfig.png')

