import xarray
from scipy.stats import norm
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

list_indices = ['tasmax']
indices = list_indices[0]

exp = ['CTL_E0', '121GPsc_E0']
exp1 = '121GPsc_E0' 

for i,ind in enumerate(exp):                                                                                                                                                                            
#print ind

#files = sorted(glob.glob('/g/data3/w97/dc8106/AMZ_def_EXPs/'+exp+'/tasmax_sc-only_1978-2011_'+exp+'.nc', chunks={'time':1000})
#analysis/ensmean/'+indices+'/'+indices+'**_*diff_to_CTL.nc'))
    data = xarray.open_dataset('/g/data3/w97/dc8106/AMZ_def_EXPs/'+exp[i]+'/tasmax_sc-only_1978-2011_'+exp[i]+'.nc', chunks={'time':1000})
#data1 = xarray.open_dataset('/g/data3/w97/dc8106/AMZ_def_EXPs/'+exp1+'/tasmax_sc-only_1978-2011_'+exp1+'.nc', chunks={'time':1000})
    tasmax = data.tasmax - 272.15
#tasmax1 = data1.tasmax - 272.15
#tasmin = data.tasmin

    lat = data.lat
    lon = data.lon
    lons,lats = np.meshgrid(lon,lat)

    ind_label = indices

    print(tasmax)
    print("tasmax")
    print(tasmax.stack(dim=["lat","lon","time"]))

    mu, sigma = tasmax.mean().values, tasmax.std().values

# Print the values of mu and sigma which forces them to be evaluated so I can see how long it takes to do this, then I can tune the time chunking
    print(mu,sigma)

# the histogram of the data                                                                                                                                                                                  
    n, bins, patches = plt.hist(tasmax.stack(dim=["lat","lon","time"]), bins = 1000, normed=1, facecolor='green', alpha=0.75)
    plt.xticks(np.arange(20, 50, 2.0))
    print(n)
    print(bins)
    print(patches)

# add a 'best fit' line                                                                                                                                                                                      
    y = mlab.normpdf( bins, mu, sigma)
    print(y)

    l = plt.plot(bins, y, 'r--', label=exp[0], linewidth=1)
    #l_legend = plt.legend(handles=l, loc=1)
l1 = plt.plot(bins, y, 'b--', label=exp[1], linewidth=1) 
#l1_legend = plt.legend(handles=l1, loc=1)

plt.legend(bbox_to_anchor=(1, 1), loc=1, borderaxespad=0.)
units = 'Celsius'

plt.axis([20, 50, 0, 0.18])
plt.xlabel(indices+' in '+units)

plt.suptitle(ind_label+ ' in ' +ind, fontsize=16)                                                                                                                                                    
                                                                                                                                                                                                           
plt.savefig('/g/data3/w97/dc8106/images/'+ind_label+'_'+exp[0]+'_'+exp[1], format='png')   

# plt.ylabel('Probability')
# plt.title(r'$\mathrm{Histogram of '+indices+'\ \mu='+mu+',\ \sigma='+sigma+')')
#plt.axis([25, 45, 0, 0.03])                                                                                                                                                                                 
#plt.grid(True)                                                                                                                                                                                              

plt.show()
