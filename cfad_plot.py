import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from netCDF4 import Dataset

import iris
import iris.plot as iplt
import iris.quickplot as qplt
from iris.analysis.cartography import unrotate_pole
import datetime



if __name__=="__main__":

	level = iris.Constraint(name='radar_reflectivity_due_to_all_hydrometeor_species',model_level_number=37)
	cube = iris.load_cube("/gws/nopw/j04/dcmex/users/msun/darwin-small/20051130T1200Z_Darwin_km1p5_RAL3p2_504p4_p2.pp",level)
	time = cube.coord('time')

	"""
		create the CFAD plots for comparison with the radar
	"""
	# 1. loop over all times and all levels
	# 2. search for lat long in the radar domain
	# 3. calculate fraction of domain > 10 dBZ
	pole_lat=77.5920 # can find by the ncdump command
	pole_lon=130.8800 #or whatever you have

	rotated_lons=cube.coord('grid_longitude').points   #sometimes this is grid_longitude in iris file....
	rotated_lats=cube.coord('grid_latitude').points

	rlats=np.array([rotated_lats,]*len(rotated_lons)).transpose()
	rlons=np.array([rotated_lons,]*len(rotated_lats))

	#get real lats and lons
	lons, lats = unrotate_pole(rlons, rlats, pole_lon, pole_lat)

	# 2. search for lat / long in the radar domain
	ind1, = np.where((lons[0]>=129.5) & (lons[0]<=131.6))
	ind2, = np.where((lats[0]>=-12) & (lats[0] < -11.2))

	# create an empty array to store values
	array = np.zeros((cube.shape[0],70))
	
	# loop over all heights
	for i in range(70):
		print('height level ' + str(i+1) + ' of ' + str(70))
 
		level = iris.Constraint(name='radar_reflectivity_due_to_all_hydrometeor_species',model_level_number=(i+1))
		cube = iris.load_cube("/gws/nopw/j04/dcmex/users/msun/darwin-small/20051130T1200Z_Darwin_km1p5_RAL3p2_504p4_p2.pp",level)
		
		for j in range(cube.shape[0]):
			dat=cube.data[j,:,:].flatten()	
			ind,=np.where(dat > 10)
			array[j,i]=len(ind) / len(dat)

	plt.ion()
	plt.pcolormesh(time.points,cube[0].aux_coords[3].points, array.T)
	plt.clim((0,1))
	plt.colorbar()
	plt.xlabel('time')
	plt.ylabel('height (m)')
	plt.savefig('my_cfad.png')



