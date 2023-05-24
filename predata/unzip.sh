#!/bin/bash

#to unzip downloaded era5 or era5land

#var=2m_temperature
#fvar=t2m
#var=2m_dewpoint_temperature
#fvar=d2m
#var=surface_pressure
#fvar=sp
#var=boundary_layer_height
#fvar=blh
#var=10m_u_component_of_wind
#fvar=u10
#var=10m_v_component_of_wind
#fvar=v10

for yr in {2022..2022} ;
  do
   for mon in {01..12} ;
   do
    
         echo unzip ${var}_${yr}.${mon}    
         unzip ./${var}_${yr}.${mon}.zip
     
     mv data.nc ../../data/era5land/${fvar}.${yr}${mon}.nc  
   done

done

