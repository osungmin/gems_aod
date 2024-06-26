#!/usr/bin/env python
import pandas as pd
import numpy as np
import os
from datetime import datetime
from netCDF4 import Dataset
print ("modules imported")


def load_idxs():
   fpath='your_meta_data_path/'
   load=pd.read_csv(fpath,
		             header=0, index_col=0)
   print(" >>> loading the meta", load.shape)
   return(load)

def create_daterange(date0, date1, freq):
   start = datetime.strptime(date0, '%Y-%m-%d')
   end = datetime.strptime(date1, '%Y-%m-%d')
   daterange366 = pd.date_range(start, end, freq=freq) # D: daily
   daterange = daterange366[~((daterange366.month == 2) & (daterange366.day == 29))]
   return(daterange, daterange366)

def extract_era(var):
  print(" \n>>> extract meteo data from ear5/era5land")
  meta=load_idxs() #table of station id | latitude | longitude
  idxs, lats, lons = meta.index, meta['lat'].values, meta['lon'].values
  daterange = create_daterange("2022-01-01", "2023-01-01", "H")[1][:-1]
  if var in ['boundary_layer_height']: inpath="../data/era5/"
  else: inpath="your_era_path/"
  outpath="your_output_path/"

  ### extract data
  nc_files=[]

  print(" >> load ncfiles")
  for yr in np.arange(daterange.year[0], daterange.year[-1]+1, 1):
	  print(" -", yr)

	  for mon in np.arange(1,12+1,1):
		  print("  ", mon)
		  f=Dataset(inpath+var+"."+str(yr)+str(mon).zfill(2)+".nc", 'r')
		  #print(f.variables)

		  if var=='2m_temperature': fvar='t2m'
		  if var=='2m_dewpoint_temperature': fvar='d2m'
		  if var=='surface_pressure': fvar='sp'
		  if var=='boundary_layer_height': fvar='blh'
		  if var=='u': fvar='u10'
		  if var=='v': fvar='v10'

		  nc=f.variables[fvar][:,:,:].filled(np.nan)
		  nc_files.append(nc)

		  if (yr==daterange.year[-1])&(mon==12):
			  datalons = f.variables['longitude'][:]
			  datalats = f.variables['latitude'][:]

		  f.close()

  print(" >> append the data")
  append = np.concatenate(nc_files, axis=0)
  print("done.", append.shape)

  print(" >> extract data at idxs")
  for idx in range(len(idxs)):
	  target={"lat":lats[idx], "lon":lons[idx]}

	  if os.path.exists(outpath+fvar+"_"+str(idxs[idx])+".dat"):
		  print (" alreay prepared!!!")
		  continue

	  #output tong
	  df=pd.DataFrame(index=daterange, columns=[fvar])

	  #
	  lat_idx = (np.abs(datalats - target["lat"])).argmin()
	  lon_idx = (np.abs(datalons - target["lon"])).argmin()

	  #
	  if idx%50==0: print (" ...", idx, idxs[idx], " out of", len(idxs))
	  if idx==0: print(" just2check", target["lat"], target["lon"], datalats[lat_idx], datalons[lon_idx])

	  df[fvar]= append[:,lat_idx,lon_idx]

	  df.to_csv(outpath+fvar+"_"+str(idxs[idx])+".dat",
			  float_format='%.2f',
			  index=True, header=True,
			  sep=",", na_rep=-9999)

  print("end", fvar, outpath)



### extract meteo data from era5/ear5land
vars=['2m_temperature','2m_dewpoint_temperature','boundary_layer_height','u','v']
for var in vars:
    extract_era(var, opt)
