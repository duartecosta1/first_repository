
# Import libraries
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import BoundaryNorm
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import matplotlib as mpl


runame = 'SAmerica_CORDEX_Noah-MP'
#'CONUS-RRTM_1hourly'
#'SAmerica_CORDEX_Noah-MP'                                                                                                                     
varib = ('SST', 'T2', 'PSFC')
var = str(varib[1])
v = str(varib[1])
path = '/g/data3/w97/dc8106/WRF_runs/Era-Interim/VALIDATION/'
wrf = path+var+'/'+runame+'_'+var+'_sept2012_remapnn.nc'
#'/CONUS-RRTM_1hourly_T2_1day-only_remapnn.nc'
#                                                                                                     
#wrf = path+var+'/wrfout_1hourly_11sep2012.nc'                                                                                                 
obs = path+'Erai-variables/T2_erai_sept2012_SAmerica.nc'
diff = path+var+'/'+runame+'_'+var+'_diff_sept2012_rightint.nc'
#'_DIFF_TO_erai_1day-only.nc'
#'/T2_diff_sept2012_rightint.nc'                                                                                                               

w = xr.open_dataset(wrf)
o = xr.open_dataset(obs)
#d = xr.open_dataset(diff)

#T2                                                                                                                                            
#start on the 1st of September
wvar = w.T2[20:].squeeze()                                                                                                                     
#wT2 = w.T2

#start on the 11th of September
#oT2 = o.tas[40:].squeeze()  
ovar = o.tas
wvar.shape
ovar.shape
str(wvar.XTIME.values[0])[:19]
str(ovar.time.values[0])[:19]
wvar = wvar.rename({'XTIME': 'time'})

#Difference between model and obs (ERA INTERIM)
d = wvar-ovar
dvar = d


lats = w.lat
lons = w.lon
#date = w.XTIME[20:].squeeze()                                                                                                                 
date = w.XTIME

olats = o.lat
olons = o.lon


panel_titles = ('WRF','Erai-Interim','Diff')
ylabel = ('00h UTC','06h UTC','12h UTC','18h UTC')



# Plot figure with subplots of different sizes
fig = plt.figure(1)
# set up subplot grid
gridspec.GridSpec(6,6)

vmin=273
vmax=313
tot_levels=11
levels = list(np.linspace(vmin,vmax,tot_levels))
custom_cmap = plt.get_cmap('afmhot_r')
norm = BoundaryNorm(levels, ncolors=custom_cmap.N, clip=True)



# large subplot - 6hourly obs (Era-Interim)
axOBS = plt.subplot2grid((6,6), (1,2), colspan=2, rowspan=3)
m = Basemap(projection='cyl',llcrnrlat=-60.,urcrnrlat=20.,llcrnrlon=-90.,urcrnrlon=-20., lon_0=0, resolution='i', ax=axOBS)
m.drawcountries(linewidth=0.25)
m.drawcoastlines(linewidth=0.50)
h = m.pcolormesh(lons,lats,oT2[20,:,:], cmap=custom_cmap, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
df = pd.DataFrame({'col0': [0, 2, 4, 6, 8, 10], 'col1': [1, 3, 5, 7, 9, 11]}, index=['0', '1', '2', '3', '4', '5'])
#small subplots to the left - 30min-ly WRF
for i in range (1):
	date_title=str(date.values[0+i])[:10]
	hour_title=str(date.values[0+i])[10:19]
	plt.suptitle(date_title +' '+runame+'\n'+hour_title, fontsize=16)
	axOBS.set_ylabel(hour_title)
	axOBS.set_title(panel_titles[1])
#   col0  col1
#0     0     1
#1     2     3
#2     4     5
#3     6     7
#4     8     9
#5    10    11

for row in range(6):
	for col in range(2):
		ax1 = plt.subplot2grid((6,6), (row,col))
		m = Basemap(projection='cyl',llcrnrlat=-60.,urcrnrlat=20.,llcrnrlon=-90.,urcrnrlon=-20., lon_0=0, resolution='i', ax=ax1)
		m.drawcountries(linewidth=0.25)
		m.drawcoastlines(linewidth=0.50)
		j = df.iloc[row,col]
		ax1.set_ylabel(str(date.values[j])[10:16])
		print (str(wT2.XTIME.values[j])[10:19])
		h = m.pcolormesh(lons,lats,wT2[j], cmap=custom_cmap, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
		#ax1.set_title(panel_titles[0])

cax = plt.axes([0.1, 0.05, 0.46, 0.02]) #left top width height
cbar = plt.colorbar(h, cax=cax, orientation='horizontal')
cbar.set_label(wT2.units)
cbar.set_ticks(np.linspace(vmin,vmax,tot_levels))

#small subplots to the right - 30min-ly difference (WRF-Era_Interim)

vmin=-10
vmax=10
tot_levels=9
levels = list(np.linspace(vmin,vmax,tot_levels))
#custom_cmap = plt.get_cmap('bwwr')
cmap = mpl.colors.ListedColormap(['#0000ff', '#1e90ff', '#00bfff', '#ffffff', '#ffffff', '#eedd82', '#daa520', '#d2691e', '#b22222'])
#cmap.set_over('red')
#cmap.set_under('blue')
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)


for row in range(6):
	for col in range(4,6):
		ax2 = plt.subplot2grid((6,6), (row,col))
		m = Basemap(projection='cyl',llcrnrlat=-60.,urcrnrlat=20.,llcrnrlon=-90.,urcrnrlon=-20., lon_0=0, resolution='i', ax=ax2)
		m.drawcountries(linewidth=0.25)
		m.drawcoastlines(linewidth=0.50)
		j = df.iloc[row,col-4]
		ax2.set_ylabel(str(dT2.XTIME.values[j])[10:16])
		print (str(dT2.XTIME.values[j])[10:19])
		h = m.pcolormesh(lons,lats,dT2[j], cmap=cmap, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
		
cax2 = plt.axes([0.65, 0.05, 0.22, 0.02]) #left top width height
cbar2 = plt.colorbar(h, cax=cax2, orientation='horizontal')
cbar2.set_label(wvar.units)
cbar2.set_ticks(np.linspace(vmin,vmax,tot_levels))


