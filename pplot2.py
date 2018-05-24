

#### pplot2.py                                                                                                                                                                                                


from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import glob
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import BoundaryNorm
#Load in the netCDF files                                                                                                                                                                                    

#Set indices to be used and create and zero np grid to be populated with the netCDF file variables. This will assign the latter to Python variables.                                                                    
list_indices = ['tasmax']
#'hfls', 'hfss', 'rss'
indices = list_indices[0] 
#

#The np grid for the data hsa the following 5 dimensions (i,ii,iii,iv,v) 
    # i) model variable (included in list_indices above)
    # ii) experiment (included in files above)
    # iii) season
    # iv) longitude
    # v) latitude
#create an empty numpy array to be filled with the following loop. (pre-allocation phase)                                                                     

#Populate np grid with data from nc files looping through i) variables and ii) files from different experiments:

#i) Populate with data from different variables

#for a,ind in enumerate(indices):
#    print ind

files = sorted(glob.glob('/g/data3/w97/dc8106/AMZ_def_EXPs/analysis/ensmean/'+indices+'/'+indices+'**_*diff_to_CTL.nc'))
#files = sorted(glob.glob('/g/data3/w97/dc8106/AMZ_def_EXPs/analysis/ensmean/'+indices+'*''*ensmean_1978-2011.nc')) 
    #remove CTL diff to CTL file from analysis
del(files[11])
var = np.zeros((len(files),4,145,192),dtype=np.float32)
t = []


lat = Dataset(files[0]).variables['lat'][:]
lon = Dataset(files[0]).variables['lon'][:]
lons,lats = np.meshgrid(lon,lat)

#)ii) Populate with data from different experiments
for n,f in enumerate(files):
    var[n:,:,:,:] = Dataset(f).variables[indices][:,:,:] # model indicators
    print var.shape                                                                                                                   
    t.append(str(files[n][-32:-3:]))

#Define plotting conditions (titles and colourbar features and range)    
for i,f in enumerate(files):
    fig, ax = plt.subplots(2,2, figsize=(10,10))
    #n_bin = [-10., -9.,  -8.,  -7.,  -6.,  -5.,  -4.,  -3.,  -2.,  -1.,  0.,   1.,   2.,   3.,   4.,   5.,   6.,   7.,   8.,   9.,  10.]
    #custom_cmap = LinearSegmentedColormap.from_list(name='custom_div_cmap', colors=[(0,0,1), (0.5,0.5,1), 'White', 'White', (1,0.5,0.5), (1,0,0)], N = 21)
    tot_levels=11
    custom_cmap = plt.get_cmap('bwr')
#('YlGnBu') -
#('BrBG')
#('PRGn')

    #custom_cmap = LinearSegmentedColormap.from_list(name='custom', colors= 'BrBG', N =tot_levels)
    panelnr = 0
    panel_titles = ('DJF','MAM','JJA','SON')
    ind_label = files[i][50:56:]
#Define conditions for the maps in 4 panels (corresponding to 4 seasons)
    for row in range(2):
        for col in range(2):

####################################################                                                                                                                                                         
# 4 seasonal PANELS                                                                                                                                                                          
####################################################                                                                                                                                                         
            m = Basemap(projection='cyl',llcrnrlat=-60.,urcrnrlat=20.,llcrnrlon=-90.,urcrnrlon=-20., lon_0=0, resolution='i', ax=ax[row, col])
            m.drawmapboundary(fill_color='white')
            m.drawcountries(linewidth=0.25)
            m.drawparallels(np.arange(-90., 99., 30.), zorder=0, color='k')
            m.drawmeridians(np.arange(-180., 180., 60.), zorder=0, color='k')
            m.drawcoastlines(linewidth=1)
         #Define min and max levels in colour bar benchmarking plotted data
            vmin=-5
            vmax=5
            levels = list(np.linspace(vmin,vmax,tot_levels))
         #Normalise to only show those levels
            norm = BoundaryNorm(levels, ncolors=custom_cmap.N, clip=True)
            h = m.pcolormesh(lons,lats,var[i, panelnr], cmap=custom_cmap, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
         #set dashed squares of weakly and strongly coupled regions (wc and sc respectively)
            wc = m.plot([-78.75, -78.75, -60, -60, -78.75], [-8.75, 3.75, 3.75, -8.75, -8.75], latlon=True, color='black', linestyle='--')
            sc = m.plot([-58.125, -58.125, -39.375, -39.375, -58.125], [-13.75, -1.25, -1.25, -13.75, -13.75], latlon=True, color='black', linestyle='--')
         #set plot season labels
            ax[row, col].set_title(panel_titles[panelnr], fontsize=11)

            panelnr += 1



    plt.suptitle(ind_label +' in '+t[i], fontsize=16)
 
   #common color bar                                                                                                                                                                                         
    cax = plt.axes([0.3, 0.05, 0.44, 0.02]) #left top width height
    cbar = plt.colorbar(h, cax=cax, orientation='horizontal')
    cbar.set_label(indices)
    cbar.set_ticks(np.linspace(vmin,vmax,tot_levels))
    plt.savefig('/g/data3/w97/dc8106/images/'+ind_label+'_ensmean_'+t[i], format='png')
    i += 1

plt.show()



