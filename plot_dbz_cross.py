#import cartopy.crs as ccrs
#import cartopy.io.shapereader as shpreader
#from cartopy.feature import NaturalEarthFeather, COLORS
#from cartopy.mpl.gridliner import LatitudeFormatter, LongitudeFormatter

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import from_levels_and_colors
from matplotlib.cm import get_cmap


import numpy as np
import xarray as xr
from netCDF4 import Dataset

import iris
import iris.plot as iplt
import iris.quickplot as qplt
from iris.analysis.cartography import unrotate_pole

#读取变量
level = iris.Constraint(name='radar_reflectivity_due_to_all_hydrometeor_species')
cube = iris.load_cube("/gws/nopw/j04/dcmex/users/msun/darwin-srtm/20051130T1200Z_Darwin_km1p5_RAL3p2_504p4_py.pp",level)  #cube(time,model_level_number,grid_latitude,grid_longitude)
#ds_var = xr.DataArray.from_iris(cube[0:35])
#ds_var = xr.DataArray.from_iris(cube[32])

#lons = cube.coord('grid_longitude').points  #sometimes this is grid_longitude in iris file....
#lats = cube.coord('grid_latitude').points
# heights = cube.coord('model_level_number').points
heights=cube[0].aux_coords[3].points # actual height

pole_lat=77.5920 # can find by the ncdump command
pole_lon=130.8800 #or whatever you have

rotated_lons=cube.coord('grid_longitude').points   #sometimes this is grid_longitude in iris file....
rotated_lats=cube.coord('grid_latitude').points

rlats=np.array([rotated_lats,]*len(rotated_lons)).transpose()
rlons=np.array([rotated_lons,]*len(rotated_lats))

#get real lats and lons
lons, lats = unrotate_pole(rlons, rlats, pole_lon, pole_lat)

#lons = np.array(lons[0])
#lats = np.array(lats[0])
lats = np.array(lats[0:900,0])  #转换为正确的经/纬度，作为剖面图的横坐标
lons = np.array(lons[0,0:900])
#垂直剖面的起始经纬度
#cross_start = CoordPair(lat=-13.8,lon=131.1)
#cross_end   = CoordPair(lat=-13.7,lon=132.2)

#插值前转化成对数（no need）
# z = 10**(cube.data/10.)
# dbz_cross = 10.0*np.log10(z_cross)

# Extract a single height vs longitude cross-section. 
#cross_section = next(cube.slices(["grid_longitude", "model_level_number"]))
#cross_section = next(cube.slices(["grid_latitude", "level_height"]))   #latitude
cross_section = next(cube[15,:,438,:].slices(["grid_longitude", "level_height"]))   #longitude  ,time=32, lat=342(grid_lat),lons=390:815(不能这样设置，必须与grid_longitude长度一致)
#print(cross_section) #radar_reflectivity_due_to_all_hydrometeor_species / (dBZ) (grid_longitude: 900; model_level_number: 80)
cross_section_1 = np.transpose(np.array(cross_section.data))  #矩阵转置

fig = plt.figure()

ax = plt.axes()


#dbz = ax.contourf(heights,lons,cross_section.data,)
dbz_range = np.arange(0,60+1,5)
dbz = ax.contourf(lons,heights,cross_section_1,levels=dbz_range,cmap="Spectral_r")   #longitude
#dbz = ax.contourf(lats,heights,cross_section_1,cmap="Spectral_r")   #latitude
#ax.set_extent([180, 186, 0, 80],)
#ax.set_xticks([182, 184, 186, 188])

cbar = fig.colorbar(dbz)
#plt.xlabel('latitude')
plt.xlabel('longitude')
plt.ylabel('height')
#plt.ylabel('model level number')
#plt.show()

#qplt.contourf(cross_section, coords=["grid_longitude", "model_level_number"], cmap="RdBu_r",)
#iplt.show()
plt.savefig('./myfig_dbz_cross.png')


#if __name__ == "__main__":
#    main()