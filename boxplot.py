from netCDF4 import Dataset
import xarray
import numpy as np
import matplotlib.pyplot as plt
data = xarray.open_dataset('txx_climatology_sc-only_1978-2011_121GPsc_ensmean.nc', chunks={'time':1000})
txx = data.txx
lat = Dataset('txx_climatology_sc-only_1978-2011_121GPsc_ensmean.nc').variables['lat'][:]
lon = Dataset('txx_climatology_sc-only_1978-2011_121GPsc_ensmean.nc').variables['lon'][:]
lon = Dataset('txx_climatology_sc-only_1978-2011_121GPsc_ensmean.nc').variables['lon'][:]

lon = Dataset('txx_climatology_sc-only_1978-2011_121GPsc_ensmean.nc').variables['lon'][:]
lons,lats = np.meshgrid(lon,lat) 

#Stack latitudinal variability together

txx.stack(dim=["lon","lat"])