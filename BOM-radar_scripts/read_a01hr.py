from mpl_toolkits.basemap import Basemap, cm
import numpy as np
import matplotlib.pyplot as plt
import datetime


def read_file(fileName='/Volumes/Database3/' + \
	'ACTIVE/PROCESSED/current/BOM-RADAR/' + \
	'a01hr/20051130/a01hr_20051130.06_e0.51_rbKZ.ascii'):

	# dictionary to hold data
	data1=dict()
	
	fp = open(fileName,'r')
	
	str1=fp.read()
	
	# break up header into useful info.
	header=str1[30:119].split()
	data1['lat_centre']=float(header[0])+float(header[1])/60.0+ \
		float(header[2])/3600.0
	
	data1['lon_centre']=float(header[3])+float(header[4])/60.0+ \
		float(header[5])/3600.0
	
	data1['date_time']=datetime.datetime.strptime(header[6] + \
		' ' + header[7],"%Y/%m/%d %H:%M:%S")
	
	# I think this is the height of the precip scan?
	data1['height']=float(header[8]) 
	
	data1['xl']=float(header[9])
	data1['xu']=float(header[10])
	data1['yl']=float(header[13])
	data1['yu']=float(header[14])
	data1['il']=int(header[11])
	data1['iu']=int(header[12])
	data1['jl']=int(header[15])
	data1['ju']=int(header[16])
	
	# the data
	dat1=str1[120:].split()
	ntot=data1['iu']*data1['ju']
	temp=[float(dat1[i]) for i in range(ntot) ]
	temp=np.array(temp)
	data1['precip_accum']=temp.reshape((data1['ju'],data1['iu']))
	ind1,ind2=np.where(data1['precip_accum']==-99.99)
	data1['precip_accum'][ind1,ind2]=np.nan
# 	ind1,ind2=np.where(data1['precip_accum']==0.0)
# 	data1['precip_accum'][ind1,ind2]=np.nan

	data1['xs']=np.linspace(data1['xl'],data1['xu'],data1['iu'])
	data1['ys']=np.linspace(data1['yl'],data1['yu'],data1['ju'])

	X,Y=np.meshgrid(data1['xs'],data1['ys'])
	Re=6.371e6
	data1['lat']=data1['lat_centre']+1000.0*Y/Re*180.0/np.pi
	data1['lon']=data1['lon_centre'] + \
		1000.0*X/(Re*np.cos(data1['lat']*np.pi/180.0))*180.0/np.pi
	data1['Re']=Re
	fp.close()
	return (data1)

if __name__=="__main__":
	data=read_file()
	
	plt.ion()
	
# create polar stereographic Basemap instance.
	m = Basemap(projection="lcc",\
		llcrnrlon=np.min(data['lon']), \
		llcrnrlat=np.min(data['lat']), \
		urcrnrlon=np.max(data['lon']), urcrnrlat=np.max(data['lat']), \
		lat_0=data['lat_centre'], lon_0=data['lon_centre'], \
		resolution='i')	
	m.drawcoastlines()
	xx,yy=m(data['lon'],data['lat'])
	m.contourf(xx,yy,data['precip_accum'])
# 	plt.axis('equal')
	cbar=m.colorbar()
# 	plt.clim((0,60))