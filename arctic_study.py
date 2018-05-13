import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')

from scipy import stats
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_validate
from sklearn.linear_model import RidgeCV
import functools

from sklearn.linear_model import Ridge, Lasso, ElasticNet

class CleanData():

    def __init__(self, data, columns_to_keep):
        self.data = data
        self.columns_to_keep = columns_to_keep
        #self.apply_functions()

    def apply_functions(self):

        self.read_data()
        self.clean_data()
        self.get_percentage_missing()
        self.replace_nulls()
        return self.df

    def read_data(self):
        self.df = pd.read_csv(self.data)

    def clean_data(self):
        self.df = self.df.replace([-9999, -999, -8888, -888, -7777, -777, -6666, -666],np.NaN)
        self.df = self.df[self.columns_to_keep]

    def get_percentage_missing(self):
        df_with_any_null_values = self.df[self.df.columns[self.df.isnull().any()].tolist()]
        num = df_with_any_null_values.isnull().sum()
        den = len(df_with_any_null_values)

        self.percent_missing = round(num/den, 2)

    def replace_nulls(self):
        for each in self.percent_missing.index:
            if self.percent_missing[each] <= 0.3:
                self.df[each].fillna((self.df[each].mean()), inplace=True)

class EDA():

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def sns_heatmap(self):#, labels):

        plt.style.use('seaborn-darkgrid')

        # Convert categorical df types into ints so corr will work
        dummy_df = pd.get_dummies(self.dataframe)
        # Compute the correlation matrix
        corr = dummy_df.corr()

        sns.set(style="white")

        # Generate a mask for the upper triangle
        mask = np.zeros_like(corr, dtype=np.bool)
        mask[np.triu_indices_from(mask)] = True

        # Set up the matplotlib figure
        f, ax = plt.subplots(figsize=(16,16))
        # Generate a custom diverging colormap
        cmap = sns.diverging_palette(220, 10, as_cmap=True)
        # Draw the heatmap with the mask and correct aspect ratio

        # Generage plot. Optional argument mask
        cm = sns.heatmap(corr, cmap=cmap, vmax=.3, center=0,
        square=True, linewidths=.5, mask=mask, cbar_kws={"shrink": .5}, annot=True, fmt='.2f', annot_kws={"size":9})#,
        #xticklabels=labels, yticklabels=labels)

        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=45)

        plt.subplots_adjust(left=0.12, bottom=0.21, right=0.86, top=0.88,
                    wspace=0.20, hspace=0.20)
        return plt

    def scatter_plot(self, column1, column2, title):

        plt.style.use('seaborn-darkgrid')

        fig, ax = plt.subplots(figsize=(14, 14))
        ax.scatter(self.dataframe[column1], self.dataframe[column2], color=["grey", 'blue'], )
        ax.set_xlabel(column1); ax.set_ylabel(column2)
        plt.style.use('seaborn-darkgrid')
        plt.title(title)

        return plt

    def nested_boxplot(self, column1, column2, title):

        plt.style.use('seaborn-darkgrid')

        sns.set(style="ticks")
        plt.figure(figsize=(15,15))
        sns.boxplot(x=column1, y=column2, data=self.dataframe, palette='PuBuGn_d')
        sns.despine(offset=10, trim=True)
        plt.xticks(rotation=45)
        plt.title(title)

        return plt

    def histogram(self, column, title):

        plt.style.use('seaborn-darkgrid')

        fig = plt.figure(figsize=(14,14))
        ax = fig.add_subplot(111)
        plt.style.use('seaborn-darkgrid')
        ax.hist(self.dataframe[column], bins=25, alpha=0.5, normed=True)
        plt.title(title)
        plt.xlabel(column)
        plt.ylabel('counts')

        return plt

    def histogram_overlay(self, df1, df2, column, title):

        plt.style.use('seaborn-darkgrid')

        fig = plt.figure(figsize=(14,14))
        ax = fig.add_subplot(111)
        ax.hist(df1[column], bins=25, alpha=0.5, label='1974-1997', color='red', normed=True)
        ax.hist(df2[column], bins=25, alpha=0.5, label='1998-2013', color='black', normed=True)
        plt.legend(loc='upper right')
        plt.xlabel("Temperature(C)")
        plt.ylabel('Counts')
        plt.title(title)

        return plt

class WelchesTTest():

    def __init__(self, a, b, title1, title2):
        self.a = a
        self.b = b
        self.a_mean = a.mean()
        self.b_mean = b.mean()
        self.title1 = title1
        self.title2 = title2

    def welches_test(self):

        welch_ttest = stats.ttest_ind(self.a, self.b, axis=0, equal_var=False)

        print(self.title1, self.a_mean)
        print(self.title2, self.b_mean)
        print("---------------------------------------------")
        print("P-value for Welch's T-test: ", welch_ttest[1])
        print('---------------------------------------------')
        print("Reject Null Hypothesis?: ", welch_ttest[1] <= 0.025)

        return welch_ttest


class Modeling():
    pass




if __name__ == '__main__':

    data_path = 'data/0-data/data_product/GLODAPv2 Arctic Ocean.csv'

    # Remove columns that indicate only quality control
    cols_to_keep = ['cruise', 'station', 'cast', 'year', 'month', 'day', 'hour', 'minute',
    'latitude', 'longitude', 'bottomdepth', 'maxsampdepth', 'bottle', 'pressure', 'depth',
    'temperature', 'theta', 'salinity', 'oxygen', 'aou', 'nitrate', 'silicate','phosphate']

    clean_df = CleanData(data_path, cols_to_keep).apply_functions()

    # I will explore whether or not there was a change in temperature
    # between the years 1974 and 2013. My idea is to bin the years
    # into two groups, and do some hypothesis testing. First, I'll
    # check for correlations that could influence my testing.

    # From the data, I saw that different temperatures were taken at
    #different depths, but these vary greatly at depths nearer the surface.
    #The depth at which temperatures were measured also varied by year.
    #I decided to choose a range in depth nearer to the surface and apply
    #that depth to both year groups. This will include greater variability in
    #temperature, but samples taken at deeper depths won't act as outliers in
    #my test.

    #There is a strong correlation between temperature and latitude,
    #as would be expected.

    # I chose year 1992 because this gives me 20 or so years in either direction.

    '''EDA'''

    heatmap = EDA(clean_df).sns_heatmap()

    temp = 'temperature'
    depth = 'depth'
    temp_depth_title = 'Temperature & Sampling Depth in Arctic Sea Between 1974 & 2013'
    temp_depth = EDA(clean_df).scatter_plot(temp, depth, temp_depth_title)

    # Separate df into years
    shallow_sample = clean_df.depth < 50.0
    recent = clean_df.year > 1997
    shallow_young = clean_df[(shallow_sample & ~recent)] #11986 samples (difference of 14,732)
    shallow_old = clean_df[(shallow_sample & recent)] #26718 samples

    # Nested boxplot to show temperature over time for all data at all depths
    x = 'year'
    y = 'temperature'
    temp_title_all_time_all_depth = "Average Arctic Sea Temperature(C) Between 1974 & 2013, Depth Range: 0-5450m"
    temp_all_depths = EDA(clean_df).nested_boxplot(x, y, temp_title_all_time_all_depth)

    # Nested boxplot to show temperature over time at the depth I am investigating
    depth_all_years = clean_df[clean_df.depth < 50]
    temp_title_all_time_my_depth = "Average Arctic Sea Temperature(C) Between 1974 & 2013, Max Depth of 50m"
    temp_all_time_my_depth = EDA(depth_all_years).nested_boxplot(x, y, temp_title_all_time_my_depth)

    # Nested boxplot to show temperature in early years shallow depth and 50m max
    temp_title_young_years = "Average Temperature(C) Between 1974 & 1997, Maximum Sample Depth of 50m"
    temp_young_years_shallow = EDA(shallow_young).nested_boxplot(x, y, temp_title_young_years)

    # Nested boxplot to show temperature in late years and shallow depth 50m max
    temp_title_old_years = "Temperature(C) Between 1998 & 2013, Maximum Sample Depth of 50m"
    temp_old_years_shallow = EDA(shallow_old).nested_boxplot(x, y, temp_title_old_years)

    # Histogram of temperature counts at 50m depth max for all years
    shallow_all = clean_df[(clean_df.depth < 50)]
    col = 'temperature'
    temp_title_all_shallow_hist = 'Arctic Sea Temperatures(c), Maximum Depth of 50m, 1974 - 2013'
    shallow_hist_all_years = EDA(shallow_all).histogram(col, temp_title_all_shallow_hist)

    # Histogram of temperature counts at 50m depth max for 1974-1997
    temp_title_young_shallow_hist = 'Arctic Sea Temperatures(C), Maximum Depth of 50m, 1974 - 1997'
    shallow_hist_young_years = EDA(shallow_young).histogram(col, temp_title_young_shallow_hist)

    # Histogram of temperature counts at 50m depth max for 1998-2013
    temp_title_old_shallow_hist = 'Arctic Sea Temperatures(C), Maximum Depth of 50m, 1998 - 2013'
    shallow_hist_old_years = EDA(shallow_old).histogram(col, temp_title_old_shallow_hist)

    # Hist of both year boxes together
    overlay_title = 'Arctic Sea Temperatures(C), Maximum Depth of 50m, (1974-1997) & (1998-2013)'
    overlay_hist = EDA(clean_df).histogram_overlay(shallow_young, shallow_old, col, overlay_title)

    '''End EDA'''

    '''Hypothesis Testing'''
    # Was there a change in average Arctic sea temperature measured at a max depth of 50m from 1972-1997 and 1998-2013?

    # Null: There was no statistically significant change in Arctic sea temperature:
    # (1972-1997), (1998-2013), 50m

    # Alternative: There was a statistically significant change in Arctic sea temperature:
    # (1972-1997), (1998-2013), 50m

    # Test type: Welch's two-tailed t-test (Welch's because of
    # unequal variance between the datasets, and because the sample
    # sizes are unequal)

    # Alpha: 0.05
    # Significance Level = 0.025


    # Welch's T-test to Determine if there was a
    # #Significant Statistical Change in Temperature in
    # #Degrees Celsius at a Maximum Sample Depth of 50 Meters
    # #from 1972-1997 & 1998-2013.

    young_year_temp = shallow_young['temperature']
    old_year_temp = shallow_old['temperature']

    welch_title1 = "Mean Temperature for 1974-1997: "
    welch_title2 = "Mean Temperature for 1998-2013: "

    test_one = WelchesTTest(young_year_temp, old_year_temp, welch_title1, welch_title2).welches_test()


    # My p-value for the Welch's Ttest was 5e-281, very small.
    # This is small enough to reject the null hypothesis that there was
    # not significant change in sea temperature at a maximum depth of 50m.

    # However, the direction of change is somewhat surprising to me.
    # My assumption was that the temperature would have increased, but the
    # mean temperature for the later years is less than half of the mean
    # temperature for the earlier years. Why could this be? If I repeat the
    # test with a different depth, what do I find?

    # Repeat at different depths, 50-2000:
    mid_sample_one = clean_df.depth > 50.0
    mid_sample_two = clean_df.depth < 2000
    recent = clean_df.year > 1997

    mid_young = clean_df[(mid_sample_one & mid_sample_two & ~recent)] #11986 samples (difference of 14,732)
    mid_old = clean_df[(mid_sample_one & mid_sample_two & recent)] #26718 samples


    # 2000-6000
    deep_sample_one = clean_df.depth > 2000
    deep_sample_two = clean_df.depth < 6000
    recent = clean_df.year > 1997

    deep_young = clean_df[(deep_sample_one & deep_sample_two & ~recent)] #11986 samples (difference of 14,732)
    deep_old = clean_df[(deep_sample_one & deep_sample_two & recent)]

    young_year_temp_deep = deep_young['temperature']
    old_year_temp_deep = deep_old['temperature']

    title_mid1 = "Mean Temperature for 1974-1997, Depth 2000-5450m: "
    title_mid2 = "Mean Temperature for 1998-2013, Depth 2000-5450m: "
    welch_ttest_deep = WelchesTTest(young_year_temp_deep, old_year_temp_deep, title_mid1, title_mid2).welches_test()

    # Again, the change in temperature is significant, but going in a direction I didn't expect.
    # I could leave it here and simply say that the ocean is getting cooler, but I decided instead to
    # Investigate whether the testing sites had changed location between the two year blocks

    # Sure enough, the sites had changed. In the 70s, it appears that the lat and log locations indicate
    # a measure from one sire of Greenland, and in later years, from the other side

    # It seems there's more investigating to do. I need to go back to the data and isolate measurements based on
    # actual testing site. If the temperature has changed at each testing site in a significant way, then I can
    # confidently say there has been a change in temperature. But until I have that information, I cannot make any
    # claims.

    # Time to go back to the data!

    '''End TTest for Now'''
