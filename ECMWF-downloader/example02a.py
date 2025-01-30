#!/usr/bin/env python
import cdsapi
c = cdsapi.Client()

str1='';
topl=60
for i in range(topl):
	if i==(topl-1):
		str1 = str1 + str(i+1)
	else:
		str1 = str1 + str(i+1) + '/'


params=[130,133,248,246,247,131,132,129, 172,235, \
	139, 170, 183, 236, 39,40,41,42,31,141,152]

str_params=''
for i in range(len(params)):
	str_params = str_params + str(params[i]) + '/'
str_params=str_params[:-1]	


dates1=['2006-02-05','2006-02-06']
times1=['00','06','12','18']

ecdata='reanalysis-era5-single-levels'
ecdata='reanalysis-era5-complete'

for i in range(len(dates1)):
	for j in range(len(times1)):
		c.retrieve(ecdata, { # Requests follow MARS syntax
												# Keywords 'expver' and 'class' can be dropped. They are obsolete
												# since their values are imposed by 'reanalysis-era5-complete'
		   'date'    : dates1[i],            # The hyphens can be omitted
		   'levelist': '1',          # 1 is top level, 137 the lowest model level in ERA5. Use '/' to separate values.
		   'levtype' : 'ml',
		   'param'   : str_params,                   # Full information at https://apps.ecmwf.int/codes/grib/param-db/
												# The native representation for temperature is spherical harmonics
		   'stream'  : 'oper',                  # Denotes ERA5. Ensemble members are selected by 'enda'
		   'time'    : times1[j],         # You can drop :00:00 and use MARS short-hand notation, instead of '00/06/12/18'
		   'type'    : 'an',
		   'grid'    : '0.75/0.75',               # Latitude/longitude. Default: spherical harmonics or reduced Gaussian grid
		   'format'  : 'grib',                # Output needs to be regular lat-lon, so only works in combination with 'grid'!
		}, 'ERA5-' + dates1[i] + '-' + times1[j] + '.grib')     # Output file. Adapt as you wish.