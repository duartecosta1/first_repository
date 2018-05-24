#from netCDF4 import Dataset

import xarray
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt

list_indices = ['tasmax']
indices = list_indices[0]

#test
#files = '/g/data3/w97/dc8106/AMZ_def_EXPs/121GPsc_E0/AMZDEF.daily_tasmin.tasmax.pr.1978_2011_121GPsc_E0.nc'
  
#remove CTL diff to CTL file from analysis                                                                                                                                                               
#del(files[11])                                                                                                                                                                                           


   
#var = np.zeros((len(files),12418,145,192),dtype=np.float32)
#t = []

data = xarray.open_dataset('/g/data3/w97/dc8106/AMZ_def_EXPs/test/tasmax_sc_001GPsc_E0_test.nc', chunks={'time':1})
tasmax = data.tasmax
#tasmin = data.tasmin
lat = data.lat
lon = data.lon
lons,lats = np.meshgrid(lon,lat)

#sc region
#lat_SC = np.where([(lat <= -1.25) & (lat >= -13.75)], [lat], [0])
#lon_SC = np.where([(lon <= -58.125) & (lon >= -39.375)], [lon], [0])
#var_SC = np.where([(lat <= -1.25) & (lat >= -13.75) & (lon <= -58.125) & (lon >= -39.375)], [tasmax], [-9999])


#)ii) Populate with data from different experiments                                                                                                                                                         
#for n,f in enumerate(files):
#var[:,:,:,:] = Dataset(files).variables[indices][:,:,:] # model indicators                                                                                                                                 
#print var.shape
#t.append(str(data[-32:-3:]))

ind_label = indices


pdf = plt.plot(tasmax, norm.pdf(tasmax))
plt.suptitle(ind_label +' in 121GPsc_E0', fontsize=16)
#plt.savefig('/g/data3/w97/dc8106/images/'+ind_label+'_ensmean_121GPsc_E0', format='png')

plt.show()
