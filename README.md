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

- GEMS AOD data; https://nesc.nier.go.kr > need to request the FTP service
- in-situ PM10 data (Korea); https://www.airkorea.or.kr
- ERA meteorological data; https://cds.climate.copernicus.eu/


# Scripts
1. ./prepdata: 
 - ./predata/airkorea/: to clean up Airkorea PM10 data
 - ./predata/era/: to download era5/land meteorological data and extract data 
 - ./predata/gems/: to extract GEMS AOD at the closest time/location to Airkorea sites
 - to prepare collocated AOD, PM10, other meteorological data

2. ./analy:
 - to fit empirical equations to AOD-PM10 data 
 - to estimate PM10 using AOD with Random Forest
 - to evaluate input importance using SHAP Values

3. ./figures:
 - to generate figures in the paper
