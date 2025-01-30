#!/usr/bin/env python
import cdsapi
c = cdsapi.Client()

str_level=''
#for i in range(137):
for i in range(59):
    str_level = str_level + str(i+1) + '/'
str_level=str_level[:-1]
#str_level='1/137'
"""
Geopotential 129
Land-sea mask 172
Skin temp 235
Surface pressure 134
Soil temp l1 139
Soil temp l2 170
Soil temp l3 183
Soil temp l4 236
Vol soil water l1 39
Vol soil water l2 40
Vol soil water l3 41
Vol soil water l4 42
Sea ice area fraction 31
"""

file_names=['Temperature', 'Specific humidity', \
	'Cloud cover','Cloud liquid water content', \
	'Cloud ice water content','U velocity','V velocity', \
	'Geopotential','Land-sea mask', 'Skin temperature', \
	'Soil temperature level 1', \
	'Soil temperature level 2', 'Soil temperature level 3', \
	'Soil temperature level 4', 'Volumetric soil water level 1', \
	'Volumetric soil water level 2', 'Volumetric soil water level 3', \
	'Volumetric soil water level 4','Sea-ice cover', \
	'Snow depth','Logarithm of surface pressure']


params=[130,133,248,246,247,131,132,129, 172,235, 134, 139, 170, 183, 236, 39,40,41,42,31,141,152]
levtype=['ml','sfc','sfc','sfc','ml','ml','ml','ml','ml','ml','ml','ml' ,'sfc']

str_params=''
for i in range(len(params)):
	str_params = str_params + str(params[i]) + '/'
str_params=str_params[:-1]	




c.retrieve('reanalysis-era5-complete', {
	'class'	 : 'ea',
			# Requests follow MARS syntax
			# Keywords 'expver' and 'class' can be dropped. They are obsolete
			# since their values are imposed by 'reanalysis-era5-complete'
   'date'    : '2006-02-05',            
			# The hyphens can be omitted
   'levelist': '1/137',      
			# 1 is top level, 137 the lowest model level in ERA5. 
			# Use '/' to separate values.
   'param'   : str_params,    
			# Full information at https://apps.ecmwf.int/codes/grib/param-db/
			# The native representation for temperature is spherical harmonics
   'stream'  : 'oper',                  
			# Denotes ERA5. Ensemble members are selected by 'enda'
   'time'    : '00/to/23/by/6',         
			# You can drop :00:00 and use MARS short-hand notation, 
			# instead of '00/06/12/18'
   'type'    : 'an',
   #'area'    : '80/-50/-25/0',          
			# North, West, South, East. Default: global
   'grid'    : '0.75/0.75',               
			# Latitude/longitude. Default: spherical harmonics or reduced Gaussian grid
   'format'  : 'grib',                
			# Output needs to be regular lat-lon, so only works in combination with 'grid'!
}, 'ERA5-2006-02-05.grib')     
	# Output file. Adapt as you wish.


