# Relationship between AOD and PM10 in South Korea revealed by XML

Our study aims to find empirical relationships between GEMS AOD satellite data and ground PM10 measurements over SKorea

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
  - gems_extract.py: to extract GEMS AOD at the closest location to Airkorea stations
  - meteo_extract.py: to extract meteorological data from ERA5 and ERA5-Land reanalysis data
  - era: to download ERA5 and ERA5-Land data
    
- analy:
  - emprical.py: to estimate PM10/PM2.5 from AOD using empirical equations and Random Forest (temporal prediction)
    - input importance is tested using SHAP
  - spatial_rf.py: to estimate PM10/PM2.5 in ungauged location using Random Forest (spatial prediction) 

- figures:
  - paper figure scripts
