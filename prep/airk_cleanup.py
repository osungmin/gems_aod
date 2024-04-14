#!/usr/bin/env python
import numpy as np
import pandas as pd
import os as os
print ("modules imported")

def read_excel(yr, q, opt=None):
    #to read Airkorea data provided in excel
    print(" \n... read_excel:", yr, q, opt)
    if opt=='mon':
        df=pd.read_excel('your_airkorea_datapath/'+str(yr)+'/'+str(yr)+str(q).zfill(2)+'.xlsx')
    else:
        df=pd.read_excel('your_airkorea_datapath/'+str(yr)+'/'+str(yr)+'q'+str(q).zfill(2)+'.xlsx',
                         na_values=-999)

    if yr in [2004]:
        df.columns=["region","st_id","st","date","SO2","CO","O3","NO2","PM10","address"]
        df['date']=df['date'].apply(lambda x: int(x[:4])*1000000+int(x[5:7])*10000+\
                                            +int(x[8:10])*100+int(x[-2:]))

    elif yr in [2017, 2019, 2020, 2021, 2022, 2023]:
        df.columns=["region","category","st_id","st","date","SO2","CO","O3","NO2","PM10","PM25","address"]
    elif yr in [2018]:
        df.columns=["region","st_id","st","date","SO2","CO","O3","NO2","PM10","PM25","address"]
    else:
        df.columns=["region","st","st_id","date","SO2","CO","O3","NO2","PM10","address"]

    df['date']=df['date'].apply(lambda x: pd.to_datetime(str(x-1), format='%Y%m%d%H'))
    print(df.describe())
    return(df)

def read_csv(yr, q):
    #to read Airkorea data provided in csv
    print(" \n... read_csv:", yr, q)
    df=pd.read_csv('your_airkorea_datapath/'+str(yr)+'q'+str(q).zfill(2)+'.csv',
                 header=0, index_col=0, na_values=-999)
    if yr<=2014: df.columns=["st_id","st","date","SO2","CO","O3","NO2","PM10","address"]
    else: df.columns=["st_id","st","date","SO2","CO","O3","NO2","PM10","PM25","address"]
    df.index=range(len(df))

    df['date']=df['date'].apply(lambda x: pd.to_datetime(str(x-1), format='%Y%m%d%H'))
    print(df.describe())
    return(df)

def split_idx(df):

    #select air quality data at each location and save it as an individual file

    #####
    idxs=np.unique(df['st_id'])
    print(" \n- split by st_id:", len(idxs))
    #####

    for idx in idxs:
      #need to modify to save PM25 from 2015
      out=df[df['st_id']==idx][["date","SO2","CO","O3","NO2","PM10","PM25"]].copy()

      f="your_output_path/"+str(idx)+".dat"
      
      if os.path.exists(f): #add data to the previous time series
          print(" > append to", f)
          out_before=pd.read_csv(f,
                         header=0, index_col=False,
                         na_values=-9999)
          out = pd.concat([out_before, out], ignore_index=True)
          out.to_csv(f, sep=',', header=True, index = False, na_rep=-9999)
        
      else: #first time series for this location
          print(" > new idx", f)
          out.to_csv(f, sep=',', header=True, index = False, na_rep=-9999)


def clean_meta():
    #to update Airkorea meta data with additional information required for the study
    meta=pd.read_csv('./AIRKOREA_aerosol_station.csv',
                      sep=';', na_values=-999)
    print(" >>> loading the meta", meta.shape)

    #list of AirKorea data (extracted for each location)
    dat_list=os.listdir('your_output_path')

    missing_meta=[]
    idxs, lats, lons, types=[],[],[],[]
    for l in dat_list:
        idx=int(l.split('.dat')[0])
        imsi=meta[meta['st_code']==idx].copy()

        if len(imsi)<1: #no information in the metadata (?)
            missing_meta.append(l)
            continue

        #print(imsi)
        idxs.append(idx)
        lats.append(imsi['lat'].values[0])
        lons.append(imsi['lon'].values[0])
        types.append(imsi['type'].values[0])

    print("done.")
    print("somehow no meta info available:", len(missing_meta))
    print(missing_meta)
    print()

    ###### save the new meta information
    df=pd.DataFrame(index=idxs, data={'lats':lats,'lons':lons, 'type':types})
    df.index.name='idx'
    print(df.describe())
    df.to_csv('./meta_airkorea.csv', sep=',',
                header=True, index=True, na_rep=-9999)
    print("end.")
    ######


##### extract aerosol data for each stations #####
for yr in np.arange(2022,2023+1):
    print()
    print(" >>>", yr)
    print()

    if yr in [2017,2019,2020,2021,2022,2023]:
      for m in range(12):
          df=read_excel(yr, m+1, opt='mon')
          split_idx(df)

    else:
      for q in range(4):
          try: df=read_excel(yr,q+1)
          except: df=read_csv(yr,q+1)
          split_idx(df)

#### I will update the Airkorea meta data
#clean_meta()
#####

print("End.")
