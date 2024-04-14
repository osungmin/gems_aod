#select variable name (era5land)
#var=surface_net_solar_radiation
#var=surface_net_thermal_radiation
#var=2m_temperature
#var=2m_dewpoint_temperature
#var=surface_pressure
#var='10m_v_component_of_wind'
#var=boundary_layer_height #era5

for yr in {2022..2023} ;
  do

  for mon in {01..12} ;

     do

     echo ${yr} ${mon} ${var}

     #either for era or eaa5land
     ./down_era5.py ${yr} ${mon} ${var}
     #./down_era5land.py ${yr} ${mon} ${var}
          
     done

done
