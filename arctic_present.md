# What's Happening in the Arctic Ocean?

#### Global Ocean Data Analysis Project
#### National Oceanic and Atmospheric Administration

Goal: Looking at data from the NOAA and GODAP, use hypothesis testing to determine whether there has been a statistically significant change in sea water temperature between the years of 1974 and 2013 in the Arctic Ocean.

### Data Cleaning & EDA

The dataset I used consisted of 123,494 rows and 101 columns before cleaning, and the dataset came with a guide book which described the various column names. The dataset can be found here[https://github.com/erindesmond/Climate-Temp/blob/master/data/0-data/data_product/GLODAPv2%20Arctic%20Ocean.csv] and the guide book can be found here[https://github.com/erindesmond/Climate-Temp/blob/master/data/0-data/Guide-1.pdf].

The columns varied between times, station id, location, latitude and longitude, sampling id, sampling depth, sampling type, and various measurements including temperature and elements, minerals, and organic matter. They also consisted of columns that indicated whether a sample had been quality controlled, and the 'score' for that quality control.

For initial cleaning before EDA, I dropped the columns indicating quality control, replaced any values of -9999 with NaN, and ended up with 23 columns.

   
