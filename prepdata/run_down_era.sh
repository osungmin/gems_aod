#select variable name (era5land or era)
#var=surface_net_solar_radiation
#var=surface_net_thermal_radiation
#var=2m_temperature
#var=2m_dewpoint_temperature
#var=surface_pressure
#var='10m_v_component_of_wind'
#var=boundary_layer_height

for yr in {2022..2022} ;
  do

  for mon in {01..12} ;

     do

     echo ${yr} ${mon} ${var}

     #either for era or eaa5land
     #./down_era.py ${yr} ${mon} ${var}
     #./down_eraland.py ${yr} ${mon} ${var}
          
     done

done
