# What's Happening in the Arctic Ocean?

#### Global Ocean Data Analysis Project
#### National Oceanic and Atmospheric Administration

Goal: Looking at data from the NOAA and GODAP, use hypothesis testing to determine whether there has been a statistically significant change in sea water temperature between the years of 1974 and 2013 in the Arctic Ocean.

### Data Cleaning

The dataset I used consisted of 123,494 rows and 101 columns before cleaning, and the dataset came with a guide book which described the various column names. The dataset can be found [here](https://github.com/erindesmond/Climate-Temp/blob/master/data/0-data/data_product/GLODAPv2%20Arctic%20Ocean.csv) and the guide book can be found [here](https://github.com/erindesmond/Climate-Temp/blob/master/data/0-data/Guide-1.pdf).

The columns varied between times, station id, location, latitude and longitude, sampling id, sampling depth, sampling type, and various measurements including temperature and elements, minerals, and organic matter. They also consisted of columns that indicated whether a sample had been quality controlled, and the 'score' for that quality control.

For initial cleaning before EDA, I dropped the columns indicating quality control, replaced any values of -9999 with NaN, and ended up with 23 columns. I then got the percentage of NaN values, and replaced the NaNs in the temperature column with the mean of temperature (there were less than 1% NaN).

### EDA

![corr_map](https://github.com/erindesmond/Climate-Temp/blob/master/arc_images/corr_heatmap.png)

You can see some relatively strong correlations with temperature in the matrix. Because my goal is to explore temperature, I want to keep these in mind. Depth seems to be an indicator for temperature; further, temperature near the surface of the ocean will likely have more variability than temperature in the depths. (It does, I checked). So, I'll organize my hypothesis test with this in mind.

![scc_all](https://github.com/erindesmond/Climate-Temp/blob/master/arc_images/depth_temp_all_scatter.png)

![temp_all_box](https://github.com/erindesmond/Climate-Temp/blob/master/arc_images/temp_all_box.png)

I decided to pick a shallow depth of 50 meters maximum for initial analysis.

![temp_mydepth_all](https://github.com/erindesmond/Climate-Temp/blob/master/arc_images/temp_all_box_mydepth.png)

![temp_young_mydepth](https://github.com/erindesmond/Climate-Temp/blob/master/arc_images/temp_young_mydepth.png)

![temp_old_mydepth](https://github.com/erindesmond/Climate-Temp/blob/master/arc_images/temp_old_mydepth.png)

![hist_all_mydepth](https://github.com/erindesmond/Climate-Temp/blob/master/arc_images/hist_all_mydepth.png)

![hist_young_mydepth](https://github.com/erindesmond/Climate-Temp/blob/master/arc_images/hist_young_mydepth.png)

![hist_old_mydepth](https://github.com/erindesmond/Climate-Temp/blob/master/arc_images/hist_old_mydepth.png)

![hist_both_mydepth](https://github.com/erindesmond/Climate-Temp/blob/master/arc_images/hist_youngold_mydepth.png)

### Hypothesis Testing

  * Null: There was no statistically significant change in Arctic Ocean temperature: (1974-1997) & (1998-2013), 50m max depth.
  * Alternative: There was a statistically significant change in Arctic Ocean temperature: (1974-1997) & (1998-2013), 50m max depth.
  * Test type: Welch's two-tailed t-test (unequal variance and sample size)
  * Alpha: 0.05
  * Significance Level: 0.025

### Welch's Test Results

  * Mean Temperature for 1974-1997:  2.678
  * Mean Temperature for 1998-2013:  1.029
  * P-value for Welch's T-test:  2.214e-247
  * Reject Null Hypothesis?: Yes

### What?

I would have assumed that the mean for 1998-2013 would have been greater than the mean for 1974-1997. So, I decided to re-do the test with various depths.

  * Depth 50m - 2000m
  * Mean Temperature for 1974-1997: 0.947
  * Mean Temperature for 1998-2013: 0.165
  * P-value for Welch's T-test:  0.0
  * Reject Null Hypothesis?: Yes

---

  * Depth 2001m - 5450m
  * Mean Temperature for 1974-1997: -0.711
  * Mean Temperature for 1998-2013: -0.577
  * P-value for Welch's T-test:  6.210e-24
  * Reject Null Hypothesis?: Yes

### Further Investigation

In all three cases using Welch's t-test, the p-value was small enough to justify rejecting the null hypothesis. However, it is likely that there is something I am missing in the data. Are we measuring at higher latitudes in later years than we were in earlier years? Does salinity have something to do with temperature?

![corr_map](https://github.com/erindesmond/Climate-Temp/blob/master/arc_images/corr_heatmap.png)


I decided to do some further testing between the years for latitude and longitude. Before I did this, I replaced any NaN values in those columns with the mean if the NaNs were less than 30% of the column.

Null: There is no difference in these between those years.
Alt: There is a difference in these between those years.

### Results from Further Investigation

Here are the average locations at which temperatures were measured between the year blocks I chose to test those on a map:

![dist_map](https://github.com/erindesmond/Climate-Temp/blob/master/arc_images/Screen%20Shot%202018-03-15%20at%209.11.06%20PM.png)

Distance between those points: 1,683.13 miles or 2,708.74 kilometers.

As you can see, the location changes drastically. This suggests that more investigation is needed before assuming a change in temperature. I need to go back to the data, isolate stations based on location and test temperatures again.

### Next Steps

Further investigate this distance between measuring for those years. Determine if it is related to temperature, refine the study.

Do some modeling to predict temperature based on the measured elements in the data. Do salinity, phosphate, density, and others contribute to temperature?
