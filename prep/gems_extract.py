#!/usr/bin/env python
import numpy as np
import pandas as pd
import sys
import glob
import os
import datetime as dt
from calendar import monthrange
import netCDF4 as nc4

import warnings
warnings.filterwarnings("ignore")
print("modules imported")

"""
This script is to extaract GEMS AOD satellite data at given station (lat/lon)
"""

def load_meta(opt=None):
    fpath='your_station_meta_data_(station idx | lat | lon )'
    load=pd.read_csv(fpath,
                     header=0, index_col=0)
    print(" >>> loading the meta", opt, load.shape)
    return(load)

def Haversine_distance(lat1, lon1, lat2, lon2):
    d_lat = np.deg2rad(abs(lat1-lat2))
    d_lon = np.deg2rad(abs(lon1-lon2))
    a = np.sin(d_lat/2)**2+np.cos(np.deg2rad(lat1))*np.cos(np.deg2rad(lat2))*np.sin(d_lon/2)**2
    c = 2*np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return 6378206.4 * c / 1000

def read_gems(date, latlon):

    n_hour = 24
    #AOD_channel = 1  # 0: 354nm, 1: 443nm, 2: 550nm

    outpath='your_output_path/_'+str(date.year)+str(date.month).zfill(2)+'/'
    gems_path='your_gems_path/'+str(date.year)+str(date.month).zfill(2)+'/'

    #-----------------
    # Read GEMS
    #-----------------

    for hh in range(n_hour):

        #find files at each hour
        GEMS_date = date + dt.timedelta(hours=hh)
        gemsfiles = glob.glob(GEMS_date.strftime(gems_path+'GK2_GEMS_L2_%Y%m%d_%H*_*ORI.nc'))

        if len(gemsfiles)>1:
            print(" this can happend?")
            print(gemsfiles)
            wait=input()

        if gemsfiles!=[]:

            NC = nc4.Dataset(gemsfiles[0])

            lat = NC.groups['Geolocation Fields'].variables['Latitude']
            fillvalue = lat._FillValue
            lat = np.array(lat); lat[lat == fillvalue] = np.nan

            lon = NC.groups['Geolocation Fields'].variables['Longitude']
            fillvalue = lon._FillValue
            lon = np.array(lon); lon[lon == fillvalue] = np.nan

            AOD = NC.groups['Data Fields'].variables['FinalAerosolOpticalDepth']
            fillvalue = AOD._FillValue
            AOD = np.array(AOD); AOD[AOD == fillvalue] = np.nan
            AOD354 = AOD[0,:,:].copy()
            AOD443 = AOD[1,:,:].copy()
            AOD550 = AOD[2,:,:].copy()

            ALH = NC.groups['Data Fields'].variables['FinalAerosolLayerHeight']
            fillvalue = ALH._FillValue
            ALH = np.array(ALH); ALH[ALH == fillvalue] = np.nan
            ALH = ALH[:,:]

            # find GEMS pixel closest to in-situ site
            for i in range(len(meta)):

                ilat, ilon= meta['lat'].values[i], meta['lon'].values[i]
                distances = Haversine_distance(ilat,ilon,lat,lon)
                idx = np.where(distances == np.nanmin(distances))

                # first time to save aod data for a location
                f=outpath+str(meta.index[i])+'_gems.dat'
                out=pd.DataFrame(index=[gemsfiles[0].split('_')[3]+':'+gemsfiles[0].split('_')[4]],
                                 data={'aod354':AOD354[idx], 'aod443':AOD443[idx], 'aod550':AOD550[idx],
                                       'alh':ALH[idx],'distance':round(np.nanmin(distances),3)})

                if os.path.exists(f): #add data to the previous time series
                    out_before=pd.read_csv(f,
                                           header=0, index_col=0,
                                           na_values=-9999)
                    out = pd.concat([out_before, out], ignore_index=False)
                    out.to_csv(f,
                               header=True, index=True,
                               sep=',', na_rep=-9999)

                else: #first time series for this location
                    out.to_csv(f,
                               header=True, index=True,
                               sep=',', na_rep=-9999)

    print("Done.", date)


def combine_gems():

    print(" \n>>> combine gems monthly data into one file: for GEMS-AOD")

    dt_parser = lambda x: datetime.strptime(x, "%Y%m%d:%H%M")

    for i in range(len(meta)):
        idx=meta.index[i]
        if i%50==0: print(" ...", i, idx, "out of", len(meta))

        for yr in range(2022,2023+1,1):
            if yr==2022: endmon=12
            if yr==2023: endmon=6

            for mon in range(1,endmon+1,1):
                gemsdir='your_output_path/_'+str(year)+str(mon).zfill(2)+'/'
                df=pd.read_csv(gemsdir+str(idx)+'_gems.dat',
                               header=0, index_col=0,
                               parse_dates=True, date_parser=dt_parser,
                               na_values=-9999)

                if  mon==1: concat=df.copy()
                else: concat=pd.concat([concat, df.copy()], axis=0)

        #check any duplicated indexs
        #it can happen if gems_extract is accidently run more than once)
        if len(concat[concat.index.duplicated()])>0:
            print(" ERROR: duplicated data in gems_extracted", idx)
            print(idx, mon)
            print(concat[concat.index.duplicated()])
            wait=input()

        #save yearly gems data
        concat.to_csv('your_final_output_path/'+str(idx)+'_gems.dat',
                      index=True, header=True,
                      sep=",", na_rep=-9999)

    print("Done.")


#####
meta=load_meta() # table of station id | latitude | longitude
selyr=int(sys.argv[1])
selmon=int(sys.argv[2])
print(" ****** selected year and month:", selyr, selmon)
#####

##### MAIN: read gems netcdf one by one for each day #####
for mon in np.arange(int(selmon), int(selmon)+1, 1):
    print(" > working on", selyr, selmon)
    for day in np.arange(1, monthrange(selyr, mon)[1]+1,1):
        read_gems(dt.datetime(selyr,mon,day), meta.copy())

##### combine extracted monthly data into one file
combine_gems(meta)
print("End.")
