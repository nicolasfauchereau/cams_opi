#!/Users/nicolasf/anaconda/bin/python

import os
import numpy as np
from numpy import ma
from dateutil import parser
from glob import glob
import xray

nvar = 7
nlat = 72
nlon = 144

lats = np.linspace(-88.75, 88.75, num=72, endpoint=True)
lons = np.linspace(1.25, 358.75, num=144, endpoint=True)

dpath = os.path.join(os.environ['HOME'], 'data/cams_opi')

print(dpath)

lfiles = sorted(glob(os.path.join(dpath, 'cams_opi_merged.??????')))

for fname in lfiles:

    data = np.fromfile(fname, dtype=np.float32, count=nvar*nlat*nlon).byteswap().reshape((nvar,nlat,nlon))

    data = ma.masked_values(data, -999.0)

    print(data.shape)

    datestring = fname.split('.')[-1]
    date = parser.parse(datestring + "01")
    date = np.array(date)[np.newaxis,...]

    """
    creates the dataset
    """

    d = {}
    d['time'] = ('time', date)
    d['lat'] = ('lat',lats)
    d['lon'] = ('lon', lons)
    d['cams'] = (['time','lat','lon'], data[0,...][np.newaxis,...])
    d['camsn'] = (['time','lat','lon'], data[1,...][np.newaxis,...])
    d['opi'] = (['time','lat','lon'], data[2,...][np.newaxis,...])
    d['comb'] = (['time','lat','lon'], data[3,...][np.newaxis,...])
    d['xxxx'] = (['time','lat','lon'], data[4,...][np.newaxis,...])
    d['comba'] = (['time','lat','lon'], data[5,...][np.newaxis,...])
    d['gam'] = (['time','lat','lon'], data[6,...][np.newaxis,...])

    dset = xray.Dataset(d)

    """
    defines some attributes
    """

    dset.lon.attrs['long_name'] = 'Longitude'
    dset.lat.attrs['long_name'] = 'Latitude'

    dset.lon.attrs['standard_name'] = 'longitude'
    dset.lat.attrs['standard_name'] = 'latitude'

    dset.lat.attrs['units'] = 'degrees_north'
    dset.lon.attrs['units'] = 'degrees_east'

    filepath = os.path.join(dpath, 'nc/cams_opi_merged.{}.nc'.format(datestring))
    print(filepath)

    dset.to_netcdf(filepath)
