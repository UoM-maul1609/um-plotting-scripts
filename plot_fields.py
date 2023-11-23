import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import os

wkdir=os.getcwd()
os.system('mkdir /work/scratch-nopw2/msun')
os.system('cp ../20051130T1200Z_Darwin_km1p5_RAL3p2_504p4_py.nc.gz /work/scratch-nopw2/msun/')
os.chdir('/work/scratch-nopw2/msun/')
print('uncompressing file...')
os.system('gunzip 20051130T1200Z_Darwin_km1p5_RAL3p2_504p4_py.nc.gz')
print('file uncompressed')


nc=Dataset('/work/scratch-nopw2/msun/20051130T1200Z_Darwin_km1p5_RAL3p2_504p4_py.nc')

plt.figure()


plt.pcolormesh(nc['actual_longitude'][:],nc['actual_latitude'][:],\
        nc['maximum_radar_reflectivity_in_the_grid_column_due_to_all_hydrometeors'][32,:,:],shading='gouraud')
plt.xlabel('longitude')
plt.ylabel('latitude')
plt.colorbar()




#plt.show()
plt.savefig('./umnsaa_px.png')


