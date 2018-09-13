import xarray as xr
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import BoundaryNorm
from matplotlib.colors import LinearSegmentedColormap

import numpy as np

runame = '1day_valdtest'
#'SAmerica_CORDEX_Noah-MP'
#'CONUS-RRTM_1hourly'
#'SAmerica_CORDEX_Noah-MP'
varib = ('SST', 'T2', 'PSFC')
forc = ('metgrid', 'erai')
var = str(varib[2])
v = str(varib[2])
path = '/g/data3/w97/dc8106/WRF_runs/Era-Interim/VALIDATION/'
#wrf = path+var+'/SAmerica_CORDEX_Noah-MP_'+var+'_sept2012.nc'
#'/CONUS-RRTM_1hourly_T2_1day-only_remapnn.nc'
#
#wrf = path+var+'/wrfout_1hourly_11sep2012.nc'
#obs = path+'Erai-variables/'+var+'_'+forc[0]+'_sept2012_SAmerica.nc'
#diff = path+var+'/'+runame+'_'+var+'_diff_sept2012_rightint.nc'
#'_DIFF_TO_'+forc[0]+'_1day-only.nc'
#'/T2_diff_sept2012_rightint.nc'

#Input data

wrf = 'wrfout_d01_2012-08-27_00_1day_valtest.nc'
#'wrfout_d01_2012-08-27_00:00:00'
met = 'TT_lev0_metgrid_all_270812_280812_v2_remapnn.nc'
#'metgrid_all_270812_280812.nc'
w = xr.open_dataset(wrf)
#o = xr.open_dataset(obs)
o = xr.open_dataset(met)
#dif = xr.open_dataset(diff)

#T2 - Temperature at 2m
#wT2 = w.T2[20:].squeeze()
#wvar = w.PSFC
wvar = w.T2
#ovar = o.tas
ovar = o.TT[:,0,:,:]
diff = wvar

#Difference between model and observations
diff[:] = wvar.values - ovar.values
dvar = diff
#wvar = wvar.rename({'XTIME': 'Times'})
#dif = wvar-ovar
#dvar = dif
#dvar = dif.PSFC

lat = w.XLAT
lon = w.XLONG

#date = w.XTIME[20:].squeeze()
date = w.XTIME

olats = ovar.lat
olons = ovar.lon

tot_levels=11
panel_titles = ('WRF','Erai-Interim','Diff')
ylabel = ('00h UTC','06h UTC','12h UTC','18h UTC')
#custom_cmap = LinearSegmentedColormap.from_list(name='custom_div_cmap', colors=[(0,0,1), (0.5,0.5,1), 'White', 'White', (1,0.5,0.5), (1,0,0)], N = tot_levels)



for i in range(0,8,4):
	fig, ax = plt.subplots(4,3, figsize=(10,10))
	ax = ax.flatten()
	#WRF
	vmin=273
	vmax=313
	levels = list(np.linspace(vmin,vmax,tot_levels))
	custom_cmap = plt.get_cmap('Spectral_r', tot_levels)
	norm = BoundaryNorm(levels, ncolors=custom_cmap.N, clip=True)
	date_title=str(date.values[0+i])[:10]
	plt.suptitle(date_title +' '+runame, fontsize=16)
    
	#Model output maps (WRF)
    
	ax[0].set_ylabel(ylabel[0])
	m0 = Basemap(projection='cyl',llcrnrlat=-60.,urcrnrlat=20.,llcrnrlon=-90.,urcrnrlon=-20., lon_0=0, resolution='i', ax=ax[0])
	m0.drawmapboundary(fill_color='white')
	m0.drawcountries(linewidth=0.25)
	m0.drawcoastlines(linewidth=1)
	h0 = m0.pcolormesh(lons,lats,wvar[0+i], cmap=custom_cmap, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
    
	ax[3].set_ylabel(ylabel[1])
	m3 = Basemap(projection='cyl',llcrnrlat=-60.,urcrnrlat=20.,llcrnrlon=-90.,urcrnrlon=-20., lon_0=0, resolution='i', ax=ax[3])
	m3.drawmapboundary(fill_color='white')
	m3.drawcountries(linewidth=0.25)
	m3.drawparallels(np.arange(-90., 99., 30.), zorder=0, color='k')
	m3.drawmeridians(np.arange(-180., 180., 60.), zorder=0, color='k')
	m3.drawcoastlines(linewidth=1)
	h3 = m3.pcolormesh(lons,lats,wvar[1+i], cmap=custom_cmap, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
    
	ax[6].set_ylabel(ylabel[2])
	m6 = Basemap(projection='cyl',llcrnrlat=-60.,urcrnrlat=20.,llcrnrlon=-90.,urcrnrlon=-20., lon_0=0, resolution='i', ax=ax[6])
	m6.drawmapboundary(fill_color='white')
	m6.drawcountries(linewidth=0.25)
	m6.drawparallels(np.arange(-90., 99., 30.), zorder=0, color='k')
	m6.drawmeridians(np.arange(-180., 180., 60.), zorder=0, color='k')
	m6.drawcoastlines(linewidth=1)
	h6 = m6.pcolormesh(lons,lats,wvar[2+i], cmap=custom_cmap, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
    
	ax[9].set_ylabel(ylabel[3])
	m9 = Basemap(projection='cyl',llcrnrlat=-60.,urcrnrlat=20.,llcrnrlon=-90.,urcrnrlon=-20., lon_0=0, resolution='i', ax=ax[9])
	m9.drawmapboundary(fill_color='white')
	m9.drawcountries(linewidth=0.25)
	m9.drawparallels(np.arange(-90., 99., 30.), zorder=0, color='k')
	m9.drawmeridians(np.arange(-180., 180., 60.), zorder=0, color='k')
	m9.drawcoastlines(linewidth=1)
	h9 = m9.pcolormesh(lons,lats,wvar[3+i], cmap=custom_cmap, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
    
	#Obs maps (Era-Interim)
    
	ax[1].set_ylabel(ylabel[0])
	m1 = Basemap(projection='cyl',llcrnrlat=-60.,urcrnrlat=20.,llcrnrlon=-90.,urcrnrlon=-20., lon_0=0, resolution='i', ax=ax[1])
	m1.drawmapboundary(fill_color='white')
	m1.drawcountries(linewidth=0.25)
	m1.drawparallels(np.arange(-90., 99., 30.), zorder=0, color='k')
	m1.drawmeridians(np.arange(-180., 180., 60.), zorder=0, color='k')
	m1.drawcoastlines(linewidth=1)
	h1 = m1.pcolormesh(olons,olats,ovar[0+i], cmap=custom_cmap, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
    
	#hourly maps (Era-Interim only has 6hourly so obs panel has to stay frozen in same 6hourly daily panels)
	#h1 = m1.pcolormesh(olons,olats,ovar[41], cmap=custom_cmap, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
    
	ax[4].set_ylabel(ylabel[1])
	m4 = Basemap(projection='cyl',llcrnrlat=-60.,urcrnrlat=20.,llcrnrlon=-90.,urcrnrlon=-20., lon_0=0, resolution='i', ax=ax[4])
	m4.drawmapboundary(fill_color='white')
	m4.drawcountries(linewidth=0.25)
	m4.drawparallels(np.arange(-90., 99., 30.), zorder=0, color='k')
	m4.drawmeridians(np.arange(-180., 180., 60.), zorder=0, color='k')
	m4.drawcoastlines(linewidth=1)
	h4 = m4.pcolormesh(olons,olats,ovar[1+i], cmap=custom_cmap, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
     	
	#hourly maps (Era-Interim only has 6hourly so obs panel has to stay frozen in same 6hourly daily panels)
	#h4 = m4.pcolormesh(olons,olats,ovar[42], cmap=custom_cmap, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
    
	ax[7].set_ylabel(ylabel[2])
	m7 = Basemap(projection='cyl',llcrnrlat=-60.,urcrnrlat=20.,llcrnrlon=-90.,urcrnrlon=-20., lon_0=0, resolution='i', ax=ax[7])
	m7.drawmapboundary(fill_color='white')
	m7.drawcountries(linewidth=0.25)
	m7.drawparallels(np.arange(-90., 99., 30.), zorder=0, color='k')
	m7.drawmeridians(np.arange(-180., 180., 60.), zorder=0, color='k')
	m7.drawcoastlines(linewidth=1)
	h7 = m7.pcolormesh(olons,olats,ovar[2+i], cmap=custom_cmap, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
    
	#hourly maps (Era-Interim only has 6hourly so obs panel has to stay frozen in same 6hourly daily panels)
    #h7 = m7.pcolormesh(olons,olats,ovar[43], cmap=custom_cmap, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
    
	ax[10].set_ylabel(ylabel[3])
	m10 = Basemap(projection='cyl',llcrnrlat=-60.,urcrnrlat=20.,llcrnrlon=-90.,urcrnrlon=-20., lon_0=0, resolution='i', ax=ax[10])
	m10.drawmapboundary(fill_color='white')
	m10.drawcountries(linewidth=0.25)
	m10.drawparallels(np.arange(-90., 99., 30.), zorder=0, color='k')
	m10.drawmeridians(np.arange(-180., 180., 60.), zorder=0, color='k')
	m10.drawcoastlines(linewidth=1)
	h10 = m10.pcolormesh(olons,olats,ovar[3+i], cmap=custom_cmap, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
 	#hourly maps (Era-Interim only has 6hourly so obs panel has to stay frozen in same 6hourly daily panels)
	#h10 = m10.pcolormesh(olons,olats,ovar[44], cmap=custom_cmap, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
	cax = plt.axes([0.1, 0.05, 0.46, 0.02]) #left top width height
	cbar = plt.colorbar(h0, cax=cax, orientation='horizontal')
	cbar.set_label(wvar.units)
	cbar.set_ticks(np.linspace(vmin,vmax,tot_levels))
	#Diff maps
	vmin = -10
	vmax = 10
	tot_levels=9
	levels2 = list(np.linspace(vmin,vmax,tot_levels))
	custom_cmap2 = plt.get_cmap('PuOr_r', tot_levels)
	#custom_cmap2 = LinearSegmentedColormap.from_list(name='custom_div_cmap', colors=[(0,0,1), (0.5,0.5,1), 'White', 'White', (1,0.5,0.5), (1,0,0)], N = tot_levels)
	norm = BoundaryNorm(levels2, ncolors=custom_cmap2.N, clip=True)
	ax[2].set_ylabel(ylabel[0])
	m2 = Basemap(projection='cyl',llcrnrlat=-60.,urcrnrlat=20.,llcrnrlon=-90.,urcrnrlon=-20., lon_0=0, resolution='i', ax=ax[2])
	m2.drawmapboundary(fill_color='white')
	m2.drawcountries(linewidth=0.25)
	m2.drawparallels(np.arange(-90., 99., 30.), zorder=0, color='k')
	m2.drawmeridians(np.arange(-180., 180., 60.), zorder=0, color='k')
	m2.drawcoastlines(linewidth=1)
	h2 = m2.pcolormesh(olons,olats,dvar[0+i], cmap=custom_cmap2, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
    
	ax[5].set_ylabel(ylabel[1])
	m5 = Basemap(projection='cyl',llcrnrlat=-60.,urcrnrlat=20.,llcrnrlon=-90.,urcrnrlon=-20., lon_0=0, resolution='i', ax=ax[5])
	m5.drawmapboundary(fill_color='white')
	m5.drawcountries(linewidth=0.25)
	m5.drawparallels(np.arange(-90., 99., 30.), zorder=0, color='k')
	m5.drawmeridians(np.arange(-180., 180., 60.), zorder=0, color='k')
	m5.drawcoastlines(linewidth=1)
	h5 = m5.pcolormesh(olons,olats,dvar[1+i], cmap=custom_cmap2, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
    
	ax[8].set_ylabel(ylabel[2])
	m8 = Basemap(projection='cyl',llcrnrlat=-60.,urcrnrlat=20.,llcrnrlon=-90.,urcrnrlon=-20., lon_0=0, resolution='i', ax=ax[8])
	m8.drawmapboundary(fill_color='white')
	m8.drawcountries(linewidth=0.25)
	m8.drawparallels(np.arange(-90., 99., 30.), zorder=0, color='k')
	m8.drawmeridians(np.arange(-180., 180., 60.), zorder=0, color='k')
	m8.drawcoastlines(linewidth=1)
	h8 = m8.pcolormesh(olons,olats,dvar[2+i], cmap=custom_cmap2, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
    
	ax[11].set_ylabel(ylabel[3])
	m11 = Basemap(projection='cyl',llcrnrlat=-60.,urcrnrlat=20.,llcrnrlon=-90.,urcrnrlon=-20., lon_0=0, resolution='i', ax=ax[11])
	m11.drawmapboundary(fill_color='white')
	m11.drawcountries(linewidth=0.25)
	m11.drawparallels(np.arange(-90., 99., 30.), zorder=0, color='k')
	m11.drawmeridians(np.arange(-180., 180., 60.), zorder=0, color='k')
	m11.drawcoastlines(linewidth=1)
	h11 = m11.pcolormesh(olons,olats,dvar[3+i], cmap=custom_cmap2, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
    
	ax[0].set_title(panel_titles[0])
	ax[1].set_title(panel_titles[1])
	ax[2].set_title(panel_titles[2])
     
	#Cbar for absolute temp values (model and obs)
	cax2 = plt.axes([0.7, 0.05, 0.22, 0.02]) #left top width height
	cbar2 = plt.colorbar(h2, cax=cax2, orientation='horizontal')
	cbar2.set_label(dvar.units)
	cbar2.set_ticks(np.linspace(vmin,vmax,tot_levels))
    
	plt.savefig('/g/data3/w97/dc8106/WRF_runs/Era-Interim/VALIDATION/COMPARISON_PLOTS/'+runame_+'COMPARISON-plots_v2'+var+'_27aug2012_'+str(date.values[0+i])[:19], format='png')
	plt.clf()



plt.show()
