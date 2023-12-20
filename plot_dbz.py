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

level = iris.Constraint(name='radar_reflectivity_due_to_all_hydrometeor_species',model_level_number=37)
cube = iris.load_cube("/gws/nopw/j04/dcmex/users/msun/darwin-small/20051130T1200Z_Darwin_km1p5_RAL3p2_504p4_p2.pp",level)
#ds_var = xr.DataArray.from_iris(cube[0:35])
ds_var = xr.DataArray.from_iris(cube[32])  # 32: time
time = cube.coord('time')

#dbz = ds_var[32, :, :]


def main():


	pole_lat=77.5920 # can find by the ncdump command
	pole_lon=130.8800 #or whatever you have

	rotated_lons=cube.coord('grid_longitude').points   #sometimes this is grid_longitude in iris file....
	rotated_lats=cube.coord('grid_latitude').points

	rlats=np.array([rotated_lats,]*len(rotated_lons)).transpose()
	rlons=np.array([rotated_lons,]*len(rotated_lats))

	#get real lats and lons
	lons, lats = unrotate_pole(rlons, rlats, pole_lon, pole_lat)


	for i in range(0,cube.shape[0]):   # cube.shape[0] 时间个数

	  fig = plt.figure(dpi=150)

	#projection = ccrs.Mercator()   # 首先，我们指定地图投影的坐标参考系
	  crs = ccrs.PlateCarree()
	  ax = plt.axes(projection=ccrs.PlateCarree())
	#ax = plt.axes(projection=projection, frameon=True)   # 现在我们将创建具有特定投影的轴对象

	#projection = ccrs.Mercator() 
	#ax = plt.axes(projection=ccrs.PlateCarree())
	  ax.add_feature(cf.COASTLINE.with_scale("10m"), lw=0.5)
	  ax.add_feature(cf.BORDERS.with_scale("10m"), lw=0.3)

	

	#lon_min = 126
	#lon_max = 136
	#lat_min = -18
	#lat_max = -8

	#lon_min = 130  # 最小/最大经度/纬度指定地图的范围。注意，这些值是以经度和纬度来指定的。然而，我们可以用任何我们想要的经度来指定它们，但我们需要在ax.set_extent中提供适当的经度参数。
	#lon_max = 136
	#lat_min = -16
	#lat_max = -10
	  lon_min = 129.9  # 最小/最大经度/纬度指定地图的范围。注意，这些值是以经度和纬度来指定的。然而，我们可以用任何我们想要的经度来指定它们，但我们需要在ax.set_extent中提供适当的经度参数。
	  lon_max = 131.6
	  lat_min = -12
	  lat_max = -11
	  ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=crs)


	#dbz=ds_var(time='')
	#cbar_kwargs = {'orientation':'horizontal', 'shrink':0.6, "pad" : .05, 'aspect':40, 'label':'Radar reflectivity [dBZ]'}
	#dbz.plot(ax=ax, transform=ccrs.PlateCarree(), cbar_kwargs=cbar_kwargs)

	#plt.pcolormesh(lons,lats,cube.data[32,:,:],shading='gouraud')
	#plt.contourf(lons,lats,cube.data[32,:,:])
	  dbz_range = np.arange(0,60+1,5)
	  dbz = ax.contourf(lons,lats,cube.data[i,:,:],levels=dbz_range,cmap="Spectral_r")   ## 20: time
	#plt.xlabel('longitude')
	#plt.ylabel('latitude')
	#ax.coastlines()
	#plt.contourf(cube.data[10,:,:], ax=ax, transform=ccrs.PlateCarree())

	#plt.contourf(cube.data[10,:,:], ax=ax, transform=ccrs.PlateCarree())
	#data[ds_var].plot.contourf(ax=ax, transform=ccrs.PlateCarree(), cbar_kwargs=cbar_kwargs, levels=21)

	#经纬度线刻度，以2°为间隔值计算刻度值
	  ax.set_xticks(np.mgrid[lon_min:lon_max+0.2:0.2], crs=crs)
	  ax.set_yticks(np.mgrid[lat_min:lat_max+0.2:0.2], crs=crs)
	#设置刻度格式为经纬度格式
	  ax.xaxis.set_major_formatter(LongitudeFormatter())
	  ax.yaxis.set_major_formatter(LatitudeFormatter())

	#colorbar
	#cbar_ax = fig.add_axes([0.2, 0.0, 0.6, 0.05])  # Left, bottom, width, height.
	#extent = [left, right, bottom, top]
	#im = ax.imshow(dbz, ax=ax, transform=crs, cmap='RdBu_r')
	#cbar = fig.colorbar(dbz, ax=ax, extend='both', orientation='horizontal')
	
	  cbar = fig.colorbar(dbz,shrink=0.5)
	  cbar.set_label('Radar reflectivity (dBZ)')
	#cbar.colorbar(shrink=0.5)

	#plt.show()
	  #plt.savefig('./myfig.png')
	  plt.savefig("/home/users/msun/darwin-small/" + str(time.points[i]) + ".png")
	  plt.close()

if __name__ == "__main__":
    main()
