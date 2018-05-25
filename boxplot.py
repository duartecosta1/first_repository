from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
txx = Dataset('txx_climatology_sc-only_1978-2011_121GPsc_ensmean.nc').variables['txx']
lat = Dataset('txx_climatology_sc-only_1978-2011_121GPsc_ensmean.nc').variables['lat'][:]
lon = Dataset('txx_climatology_sc-only_1978-2011_121GPsc_ensmean.nc').variables['lon'][:]
lon = Dataset('txx_climatology_sc-only_1978-2011_121GPsc_ensmean.nc').variables['lon'][:]

lon = Dataset('txx_climatology_sc-only_1978-2011_121GPsc_ensmean.nc').variables['lon'][:]
lons,lats = np.meshgrid(lon,lat) 