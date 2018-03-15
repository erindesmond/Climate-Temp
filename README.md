# Tracking Global Sea Temperatures Between 1972 & 2013

##### A case study investigating data from the NOAA and GODAP.
##### I will explore the difference in global sea temperature measured
##### at various depths from the years of 1972 to 2013.
##### The case study will be split into two parts: a simply Hypothesis
##### test to determine if there was a difference in temperature between two
##### years, and a regression analysis to determine predictive features that
##### correlate to temperature.

# Datasources:

##### Global Ocean Data Analysis Project
##### National Oceanic and Atmospheric Administration


# Part 1 -  Hypothesis Testing:

#### Was there a statistically significant change in average sea temperature
#### measured at a max depth of 7682m between the years of 1972 and 2013?

##### Null: There was no statistically significant change in sea temperature between 1972 & 2013

##### Alternative: There was a statistically significant change in sea temperature between 1972 & 2013

##### Test type: Welch's two-tailed t-test
##### Alpha: 0.05
##### Significance Level = 0.025

# Part 1 - Results

##### Comparing the years 1972 and 2013, with some EDA and a Welch's T-test
##### produced a significant p-value with enough argument for rejecting the Null
##### hypothesis.  

# Part 2 - Predictive Modeling

#### Ridge, Lasso, and ElasticNet models for predicting temperature.

# Part 2 - Results

#### After modeling with Ridge, Lasso and ElasticNet, I observed that the RMSEs
#### at different values of alpha with a ratio of 0.5 between the training data #### and test data for my ElasticNet model were similar suggesting that the #### model works well.

# To-Do

#### Plot these models if possible. Make sure you understand what is happening.
#### Organize code.
#### Make presentable.
