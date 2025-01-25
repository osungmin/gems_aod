# Use of GEMS AOD data to estimate ground-level particulate matter concentrations in South Korea

Our study aims to estimate ground-level PM10/PM2.5 in South Korea using GEMS AOD satellite data

# GEMS AOD satellite data

To get familiar with the GEMS and its air quality products; 

- New Era of Air Quality Monitoring from Space: Geostationary Environment Monitoring Spectrometer (GEMS), Kim et al., BAMS, 2020
(https://doi.org/10.1175/BAMS-D-18-0013.1)
- GEMS Aerosol Retrieval Algorithm (https://nesc.nier.go.kr/ko/html/satellite/doc/doc.do)
- Webinar series by NOAA and NIER > Part 3: AQ Products from GEMS
(http://appliedsciences.nasa.gov/join-mission/training/english/arset-accessing-and-analyzing-air-quality-data-geostationary)
- Python scripts to access GEMS aerosol data
(https://github.com/NASAARSET/GEMS_AQ)


# Data availability

- GEMS AOD data; https://nesc.nier.go.kr > need to request the FTP service (now API is available!)
- in-situ PM10/PM2.5 data (Korea); https://www.airkorea.or.kr
- ERA meteorological data; https://cds.climate.copernicus.eu/


# Scripts

- prep:
  - airk_cleanup.py: to clean up Airkorea data and create a meta file (lat/lon info)
  - gems_extract.py: to extract GEMS AOD at the closest pixels to Airkorea stations
  - meteo_extract.py: to extract meteorological data from ERA5 and ERA5-Land reanalysis data
  - down_era.py, down_eraland.py: to download ERA5 and ERA5-Land data
    
- analy:
  - model_runs.py: to estimate PM10/PM2.5 from AOD using empirical equations and random forest (temporal prediction)
    - input importance is tested using SHAP
    
- figures:
  - paper figure scripts with (sample) plot data

# Reference

- We would highly appreciate if you cite our paper when you use our scripts.

Estimating​ ​hourly​ ​ground-level​ ​aerosols​ ​using​ ​GEMS​ ​aerosol​ ​optical​ ​depth:​ ​A​ ​machine​ ​learning​ ​approach (O et al., 2025) doi: 
  
