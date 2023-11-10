import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset

nc=Dataset('umnsaa_px.nc')

plt.figure()


plt.pcolormesh(nc['actual_longitude'][:],nc['actual_latitude'][:],\
        nc['toa_outgoing_longwave_flux'][-1,:,:],shading='gouraud')
plt.xlabel('longitude')
plt.ylabel('latitude')




#plt.show()
plt.savefig('./umnsaa_px.png')


