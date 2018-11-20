import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
from datetime import datetime

path = '/media/z5095724/Elements/heatwaves/Era-INTERIM/EHF/'
file2 = path+'EHF_Era-INTERIM_1979-2015.nc'

data2 = xr.open_dataset(file2)

#extract 3D variable and print dimensions
ehf = data2.t2m
ehf.shape

lat = data2.latitude[:]
lon = data2.longitude[:]-360
lons,lats = np.meshgrid(lon,lat)


#object with maximum values map, regardless of when in the year
y1988 = ehf.sel(time='1988').max('time')

#loop through years
start = '1979'
end = '2015'
total = int(end)-int(start)+1
years = np.linspace(start,end,total)
#all years max
t2m_max = t2m.sel(time=slice(start, end)).max('time')

#create array with space and time dimensions to write annual EHF max
a = xr.open_dataset(path+'EHF_yrmax_79-2015.nc')

yrmax = np.zeros_like(a.t2m[0,:,:], dtype=np.float32)

#value and time of ehf for each grid point

t = ehf[:,50,50]

date = pd.to_datetime(datetime.strptime(str(t[i].time.values)[0:10], '%Y-%m-%d'))


yrmax = xr.Dataset({'max_date': date}, coords={'lon': lon, 'lat': lat}

for lat in range(353):
        for lon in range(401):
                for i in range(4423):
                        if ehf[i,lat,lon] == ehf[:,lat,lon].max().values:
                                date = pd.to_datetime(datetime.strptime(str(ehf[i,lat,lon].time.values)[0:10], '%Y-%m-%d'))
                                date_o = date.toordinal()
                                yrmax[lat,lon] = date_o
                                date.fromordinal(date_o)
                                date_o
                        else:
                                print(str(lat)+' '+str(lon)+' '+str(i)+' not max')
                #yrmax[lat,lon] = datetime.strptime(str(t[i].time.values)[0:10], '%Y-%m-%d')

