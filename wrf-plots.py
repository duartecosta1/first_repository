from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import os
import xarray as xr
from wrf import getvar, interplevel, to_np, get_basemap, latlon_coords, ALL_TIMES
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import BoundaryNorm

# Open the NetCDF file
ncfile = Dataset("/short/w97/dc8106/WRF/WRFV3/run/wrfout_d01_2012-08-27_00:00:00")

# Extract diagnostic fields from wrfout
p = getvar(ncfile, "pressure", timeidx=ALL_TIMES)
z = getvar(ncfile, "z", units="dm", timeidx=ALL_TIMES)
ua = getvar(ncfile, "ua", units="kt", timeidx=ALL_TIMES)
va = getvar(ncfile, "va", units="kt", timeidx=ALL_TIMES)
temp = getvar(ncfile, "temp", units="degC", timeidx=ALL_TIMES)
wspd = getvar(ncfile, "wspd_wdir", units="kts", timeidx=ALL_TIMES)[0,:]
date = getvar(ncfile, "times", timeidx=ALL_TIMES)
wdir = getvar(ncfile, "wspd_wdir", units="kts", timeidx=ALL_TIMES)[1,:]
cldfra = getvar(ncfile, "cloudfrac", timeidx=ALL_TIMES)

#Save new WRF diagnostic fields as netcdf files
i = wspd
variable = (p, z, ua, va, wspd, wdir)
names = ('p', 'z', 'ua', 'va', 'wspd', 'wdir')
for n,i in enumerate(variable):
	try:
		i.attrs['projection'] = 'mercator'
		#del i.attrs['coordinates']
		save = xr.DataArray.to_netcdf(i, path='/g/data3/w97/dc8106/WRF_runs/Era-Interim/VALIDATION/'+names[n]+'.nc')
	except:
		pass


var = wspd

for t in range(0,4,4):
    fig, ax = plt.subplots(2,2, figsize=(10,10))
    panelnr = 0
    panel_titles = ('00h UTC','06h UTC','12h UTC','18h UTC')
    i = t
    for row in range(2):
        for col in range(2):          
# Interpolate geopotential height, u, and v winds to 500 hPa
            ht_500 = interplevel(z, p, 500)
            u_500 = interplevel(ua, p, 500)
            v_500 = interplevel(va, p, 500)
            wspd_500 = interplevel(wspd, p, 500)
            
            # Get the lat/lon coordinates
            lats, lons = latlon_coords(ht_500)
            
            # Get the basemap object
            bm = get_basemap(ht_500)
            
            # Create the figure
            #fig = plt.figure(figsize=(12,9))
            #ax = plt.axes()
            
            # Convert the lat/lon coordinates to x/y coordinates in the projection space
            x, y = bm(to_np(lons), to_np(lats))
            
            #norm = BoundaryNorm(levels, ncolors=custom_cmap.N, clip=True)
            #h = bm.pcolormesh(lons,lats,wspd[panelnr+i])#, cmap=custom_cmap, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
            ax[row, col].set_title(panel_titles[panelnr], fontsize=11)
            
            # Add the 500 hPa geopotential height contours
            levels = np.arange(520., 580., 6.)
            contours = bm.contour(x, y, to_np(ht_500[t,:,:]), levels=levels, colors="black")
            plt.clabel(contours, inline=1, fontsize=10, fmt="%i")
            
            # Add the wind speed contours
            levels = [25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 110, 120]
            wspd_contours = bm.contourf(x, y, to_np(wspd_500[t,:,:]), levels=levels,
                                        cmap=get_cmap("rainbow"))
            plt.colorbar(wspd_contours, ax=ax, orientation="horizontal", pad=.05)
            
            # Add the geographic boundaries
            bm.drawcoastlines(linewidth=0.25)
            #bm.drawstates(linewidth=0.25)
            bm.drawcountries(linewidth=0.50)
            		            			
            # Add the 500 hPa wind barbs, only plotting every 20th data point.
            bm.barbs(x[::20, ::20], y[::20, ::20], to_np(u_500[t, ::20, ::20]), to_np(v_500[t, ::20, ::20]), length=6)
            
            
            if panelnr == 0:        
                date_title=str(date.values[0+t])[:10]
                plt.suptitle(date_title + 'wspd', fontsize=16)
                plt.title("500 MB Height (dm), Wind Speed (kt), Barbs (kt)")
            
                print (date_title)
            else:
                date_title='date title error'
                     
            panelnr += 1
            
	#common color bar                                                                                                                                                                                         
cax = plt.axes([0.3, 0.05, 0.44, 0.02]) #left top width height
cbar = plt.colorbar(h, cax=cax, orientation='horizontal')
    #cbar.set_label('m s-1')
    #cbar.set_ticks(np.linspace(vmin,vmax,tot_levels))

#plt.savefig('/g/data3/w97/dc8106/WRF_runs/Era-Interim/VALIDATION/'+names[4]+'_'+str(date.values[0+i])[:10], format='png')

plt.show()



#ws_save = Dataset('/g/data3/w97/dc8106/WRF_runs/Era-Interim/VALIDATION/test_wspd.nc', 'w')
#ws_save = xr.DataArray.to_netcdf(wdir, path='/g/data3/w97/dc8106/WRF_runs/Era-Interim/WRF_outputs/wdir.nc', mode='w')
	
plt.savefig('/g/data3/w97/dc8106/WRF_runs/Era-Interim/VALIDATION'+str(var)+'_'+str(date.values[0+i])[:10], format='png')

