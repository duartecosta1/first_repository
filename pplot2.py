

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
list_indices = ('cld', 'hfl', 'l01', 'lwp', 'pev', 'psl', 'rnd', 'thm', 'tlf', 'tlg', 'tlm', 'tsc', 'wfb', 'wfg')
definition = ('Total cloud', 'Surface sensible heat flux', 'L01 latent heat flux', 'Liquid water path', 'Potential evapotranspiration', 'Sea-level pressure', 'Precipitation', 'Extreme maximum screen temperature', 'Daily mininum vegetated ground temperature', 'Daily minimum bare ground temperature', 'Extreme minimum screen temperature', 'Screen temperature', 'Upper level soil moisture', 'Lower level soil moisture')
units = ('fraction', 'Wm −2', 'Wm −2', 'kgm −2', 'mm/day', 'hPa', 'mm/day', 'K', 'K', 'K', 'K', 'K', 'fraction', 'fraction')
path='/home/z5095724/Documents/Clim3001/analysis/metrics'
files = sorted(glob.glob('/home/z5095724/Documents/Clim3001/analysis/metrics/''**_*diff-to-CTL.nc'))

#sorted(glob.glob)
del(files[0])
del(files[2])
#'tasmax'
#'hfls', 'hfss', 'rss'

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

    #'/g/data3/w97/dc8106/AMZ_def_EXPs/analysis/ensmean/'+indices+'/'+indices+'**_*diff_to_CTL.nc'))
#files = sorted(glob.glob('/g/data3/w97/dc8106/AMZ_def_EXPs/analysis/ensmean/'+indices+'*''*ensmean_1978-2011.nc')) 
    #remove CTL diff to CTL file from analysis

lat = Dataset(files[0]).variables['latitude'][:]
lon = Dataset(files[0]).variables['longitude'][:]
var = np.zeros((len(files),12,len(lat),len(lon)),dtype=np.float32)
t = []
lons,lats = np.meshgrid(lon,lat)

#)ii) Populate with data from different experiments
   
for n,f in enumerate(files):
    indices = list_indices[n]
    var[n:,:,:,:] = Dataset(f).variables[indices][:,:,:] # model indicators
    var.shape                                                                                                                   
    t.append(str(files[n][-20:-15:]))
    print(n)
    print(f)
        

#Define plotting conditions (titles and colourbar features and range)    
for i,f in enumerate(files):
    fig, ax = plt.subplots(4,3, figsize=(10,10))
#n_bin = [-10., -9.,  -8.,  -7.,  -6.,  -5.,  -4.,  -3.,  -2.,  -1.,  0.,   1.,   2.,   3.,   4.,   5.,   6.,   7.,   8.,   9.,  10.]
#custom_cmap = LinearSegmentedColormap.from_list(name='custom_div_cmap', colors=[(0,0,1), (0.5,0.5,1), 'White', 'White', (1,0.5,0.5), (1,0,0)], N = 21)
    tot_levels=11
    custom_cmap = plt.get_cmap('bwr')
#('YlGnBu') -
#('BrBG')
#('PRGn')
#custom_cmap = LinearSegmentedColormap.from_list(name='custom', colors= 'BrBG', N =tot_levels)
    panelnr = 0
    panel_titles = ('01','02','03','04','05','06','07','08','09','10','11','12')
#('DJF','MAM','JJA','SON')
    ind_label = files[i][-25:-21:]
#Define conditions for the maps in 4 panels (corresponding to 4 seasons)
    for row in range(4):
        for col in range(3):

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
          #Adjust spectrum of colours for fraction units
            units[i]
            if units[i] == 'fraction':
                vmin=-1
                vmax=1
            else:
                vmin=-5 
                vmax=5
            levels = list(np.linspace(vmin,vmax,tot_levels))
         #Normalise to only show those levels
            norm = BoundaryNorm(levels, ncolors=custom_cmap.N, clip=True)
            h = m.pcolormesh(lons,lats,var[i, panelnr], cmap=custom_cmap, latlon=True, vmin=vmin, vmax=vmax, norm=norm)
         #set dashed squares of weakly and strongly coupled regions (wc and sc respectively)
            #wc = m.plot([-78.75, -78.75, -60, -60, -78.75], [-8.75, 3.75, 3.75, -8.75, -8.75], latlon=True, color='black', linestyle='--')
            #sc = m.plot([-58.125, -58.125, -39.375, -39.375, -58.125], [-13.75, -1.25, -1.25, -13.75, -13.75], latlon=True, color='black', linestyle='--')
         #set plot season labels
            ax[row, col].set_title(panel_titles[panelnr], fontsize=11)
            panelnr += 1



    plt.suptitle(ind_label +' in '+definition[i], fontsize=16)
 
   #common color bar                                                                                                                                                                                         
    cax = plt.axes([0.3, 0.05, 0.44, 0.02]) #left top width height
    cbar = plt.colorbar(h, cax=cax, orientation='horizontal')
    cbar.set_label(ind_label+'_'+units[i])
    cbar.set_ticks(np.linspace(vmin,vmax,tot_levels))
    plt.savefig(path+'/'+ind_label+'_CLIM3001_diff-to-CTL_'+t[i], format='png')
    i += 1

plt.show()



