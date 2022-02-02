In this blog post, I will create interactive graphics using NOAA climate data.

## §1. Data Prep - Creating a Database

First, its easiest to import all your necessary packages


```python
import sqlite3
import numpy as np
import pandas as pd
from plotly import express as px
from sklearn.linear_model import LinearRegression
```

Next, use the pandas package to turn your csvs into a dataframe that is easily manipulated.


```python
temps = pd.read_csv("temps.csv")
cntry = pd.read_csv("countries.csv")
statn = pd.read_csv("station-metadata.csv")
```

Good data is that which is plenty and is easy to work with. We have the plenty O' data thing down now, so lets make it easy to work with :)))

The stations' dataset can lose the "STNELEV" column because we have no use for it. Also we are going to create a new column called "FIPS 10-4" because the FIPS 10-4 code is simply the first two letters of each station's ID. We will use the FIPS 10-4 code shortly.


```python
statn = statn.drop(["STNELEV"], axis = 1)
statn["FIPS 10-4"] = statn["ID"].str[0:2]
statn
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ID</th>
      <th>LATITUDE</th>
      <th>LONGITUDE</th>
      <th>NAME</th>
      <th>FIPS 10-4</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ACW00011604</td>
      <td>57.7667</td>
      <td>11.8667</td>
      <td>SAVE</td>
      <td>AC</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AE000041196</td>
      <td>25.3330</td>
      <td>55.5170</td>
      <td>SHARJAH_INTER_AIRP</td>
      <td>AE</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AEM00041184</td>
      <td>25.6170</td>
      <td>55.9330</td>
      <td>RAS_AL_KHAIMAH_INTE</td>
      <td>AE</td>
    </tr>
    <tr>
      <th>3</th>
      <td>AEM00041194</td>
      <td>25.2550</td>
      <td>55.3640</td>
      <td>DUBAI_INTL</td>
      <td>AE</td>
    </tr>
    <tr>
      <th>4</th>
      <td>AEM00041216</td>
      <td>24.4300</td>
      <td>54.4700</td>
      <td>ABU_DHABI_BATEEN_AIR</td>
      <td>AE</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>27580</th>
      <td>ZI000067983</td>
      <td>-20.2000</td>
      <td>32.6160</td>
      <td>CHIPINGE</td>
      <td>ZI</td>
    </tr>
    <tr>
      <th>27581</th>
      <td>ZI000067991</td>
      <td>-22.2170</td>
      <td>30.0000</td>
      <td>BEITBRIDGE</td>
      <td>ZI</td>
    </tr>
    <tr>
      <th>27582</th>
      <td>ZIXLT371333</td>
      <td>-17.8300</td>
      <td>31.0200</td>
      <td>HARARE_BELVEDERE</td>
      <td>ZI</td>
    </tr>
    <tr>
      <th>27583</th>
      <td>ZIXLT443557</td>
      <td>-18.9800</td>
      <td>32.4500</td>
      <td>GRAND_REEF</td>
      <td>ZI</td>
    </tr>
    <tr>
      <th>27584</th>
      <td>ZIXLT622116</td>
      <td>-19.4300</td>
      <td>29.7500</td>
      <td>GWELO</td>
      <td>ZI</td>
    </tr>
  </tbody>
</table>
<p>27585 rows × 5 columns</p>
</div>



Again, we drop unecessary columns and do a little renaming to make our table more clear.


```python
cntry = cntry.drop(["ISO 3166"], axis = 1)
cntry = cntry.rename(columns = {"Name"  : "Country"})
cntry
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>FIPS 10-4</th>
      <th>Country</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AF</td>
      <td>Afghanistan</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AX</td>
      <td>Akrotiri</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AL</td>
      <td>Albania</td>
    </tr>
    <tr>
      <th>3</th>
      <td>AG</td>
      <td>Algeria</td>
    </tr>
    <tr>
      <th>4</th>
      <td>AQ</td>
      <td>American Samoa</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>274</th>
      <td>-</td>
      <td>World</td>
    </tr>
    <tr>
      <th>275</th>
      <td>YM</td>
      <td>Yemen</td>
    </tr>
    <tr>
      <th>276</th>
      <td>-</td>
      <td>Zaire</td>
    </tr>
    <tr>
      <th>277</th>
      <td>ZA</td>
      <td>Zambia</td>
    </tr>
    <tr>
      <th>278</th>
      <td>ZI</td>
      <td>Zimbabwe</td>
    </tr>
  </tbody>
</table>
<p>279 rows × 2 columns</p>
</div>



The Temps dataset has a little more involved procedure called stacking, so I would rather comment the code step by step below.


```python
# Stacking makes data visualization easy and logical

#first we seperate any Columns that would not stack well
#we choose ID so all of IDs are placed nicely together
#we choose Year to order them chronologically
temps = temps.set_index(keys=["ID", "Year"])
temps = temps.stack()

#this will recover Month and Temp columns, making them nice and neat
temps = temps.reset_index()

#some renaming and cleaning up to make more legible
temps = temps.rename(columns = {"level_2"  : "Month" , 0 : "Temp"})
temps["Month"] = temps["Month"].str[5:].astype(int)
temps["Temp"] = temps["Temp"] / 100
temps
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ID</th>
      <th>Year</th>
      <th>Month</th>
      <th>Temp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ACW00011604</td>
      <td>1961</td>
      <td>1</td>
      <td>-0.89</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ACW00011604</td>
      <td>1961</td>
      <td>2</td>
      <td>2.36</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ACW00011604</td>
      <td>1961</td>
      <td>3</td>
      <td>4.72</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ACW00011604</td>
      <td>1961</td>
      <td>4</td>
      <td>7.73</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ACW00011604</td>
      <td>1961</td>
      <td>5</td>
      <td>11.28</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>13992657</th>
      <td>ZIXLT622116</td>
      <td>1970</td>
      <td>8</td>
      <td>15.40</td>
    </tr>
    <tr>
      <th>13992658</th>
      <td>ZIXLT622116</td>
      <td>1970</td>
      <td>9</td>
      <td>20.40</td>
    </tr>
    <tr>
      <th>13992659</th>
      <td>ZIXLT622116</td>
      <td>1970</td>
      <td>10</td>
      <td>20.30</td>
    </tr>
    <tr>
      <th>13992660</th>
      <td>ZIXLT622116</td>
      <td>1970</td>
      <td>11</td>
      <td>21.30</td>
    </tr>
    <tr>
      <th>13992661</th>
      <td>ZIXLT622116</td>
      <td>1970</td>
      <td>12</td>
      <td>21.50</td>
    </tr>
  </tbody>
</table>
<p>13992662 rows × 4 columns</p>
</div>



TA-DAA we now have three clean dataframes! 
Now... we upload into the mainframe

Ok well not actually, but we will create our own SQL database to upload our three dataframes for easy and quicker acess.


```python
#this line creates an SQL database that is much easier to index
conn = sqlite3.connect("NOAA.db")

#following lines upload our dataframes, one at a time.
cntry.to_sql("countries", conn, if_exists='append', index=False)
temps.to_sql("temperatures", conn, if_exists='append', index=False)
statn.to_sql("stations", conn, if_exists='append', index=False)
```

Alright, now to check that our data is there...


```python
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())
```

    [('countries',), ('temperatures',), ('stations',)]
    

Great! It seems our databases have turned into three seperate tables within our database!
Now just close off the connection for safety's sake.


```python
conn.close()
```

## §2. Writing A Query Function

Now to write a query function for our data.
This function will return pandas dataframe of temperature readings for the specified country, in the specified date range, in the specified month of the year.


```python
def query_climate_database(country, year_begin, year_end, month):
    '''
    This function will return pandas dataframe of temperature readings for the 
    specified country, in the specified date range, in the specified month of the year.
    
    @param country: a string giving the name of a country for which data should be returned
    @param year_begin and year_end: two integers giving the earliest and latest years for 
                                    which should be returned
    @param month: an integer giving the month of the year for which should be returned
    
    return joined: a Pandas dataframe of temperature readings for the specified country, 
                   in the specified date range, in the specified month of the year. 
    '''
    
    conn = sqlite3.connect("NOAA.db")
    cursor = conn.cursor() 
    
    #we use sqlite to join all of the important columns of our tables together using
    #the constant columns id and FIPS 10-4 (see I told you we'd use it soon.)
    cmd = \
    """
    SELECT S.NAME, S.LATITUDE, S.LONGITUDE, C.Country, T.Year, T.Month, T.Temp
    FROM stations S
    LEFT JOIN temperatures T on S.ID = T.ID, countries C on C.'FIPS 10-4' = S.'FIPS 10-4'
    WHERE C.Country = '{0}' AND T.Year>= {1} AND T.Year<= {2} AND T.Month = {3}
    """
    cmd = cmd.format(country, year_begin, year_end, month)
    joined = pd.read_sql_query(cmd, conn)
    conn.close()
    return joined

```

As you can see, our function works perfectly!


```python
query_climate_database(country = "India", 
                       year_begin = 1980, 
                       year_end = 2020,
                       month = 1)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>NAME</th>
      <th>LATITUDE</th>
      <th>LONGITUDE</th>
      <th>Country</th>
      <th>Year</th>
      <th>Month</th>
      <th>Temp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>PBO_ANANTAPUR</td>
      <td>14.583</td>
      <td>77.633</td>
      <td>India</td>
      <td>1980</td>
      <td>1</td>
      <td>23.48</td>
    </tr>
    <tr>
      <th>1</th>
      <td>PBO_ANANTAPUR</td>
      <td>14.583</td>
      <td>77.633</td>
      <td>India</td>
      <td>1980</td>
      <td>1</td>
      <td>23.48</td>
    </tr>
    <tr>
      <th>2</th>
      <td>PBO_ANANTAPUR</td>
      <td>14.583</td>
      <td>77.633</td>
      <td>India</td>
      <td>1980</td>
      <td>1</td>
      <td>23.48</td>
    </tr>
    <tr>
      <th>3</th>
      <td>PBO_ANANTAPUR</td>
      <td>14.583</td>
      <td>77.633</td>
      <td>India</td>
      <td>1980</td>
      <td>1</td>
      <td>23.48</td>
    </tr>
    <tr>
      <th>4</th>
      <td>PBO_ANANTAPUR</td>
      <td>14.583</td>
      <td>77.633</td>
      <td>India</td>
      <td>1980</td>
      <td>1</td>
      <td>23.48</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>393995</th>
      <td>DARJEELING</td>
      <td>27.050</td>
      <td>88.270</td>
      <td>India</td>
      <td>1997</td>
      <td>1</td>
      <td>5.70</td>
    </tr>
    <tr>
      <th>393996</th>
      <td>DARJEELING</td>
      <td>27.050</td>
      <td>88.270</td>
      <td>India</td>
      <td>1997</td>
      <td>1</td>
      <td>5.70</td>
    </tr>
    <tr>
      <th>393997</th>
      <td>DARJEELING</td>
      <td>27.050</td>
      <td>88.270</td>
      <td>India</td>
      <td>1997</td>
      <td>1</td>
      <td>5.70</td>
    </tr>
    <tr>
      <th>393998</th>
      <td>DARJEELING</td>
      <td>27.050</td>
      <td>88.270</td>
      <td>India</td>
      <td>1997</td>
      <td>1</td>
      <td>5.70</td>
    </tr>
    <tr>
      <th>393999</th>
      <td>DARJEELING</td>
      <td>27.050</td>
      <td>88.270</td>
      <td>India</td>
      <td>1997</td>
      <td>1</td>
      <td>5.70</td>
    </tr>
  </tbody>
</table>
<p>394000 rows × 7 columns</p>
</div>



## §3. Write a Geographic Scatter Function for Yearly Temperature Increases

Now we want to find the year-over-year average change in temperature. How can we do that you ask? A little mathmatical model called Linear Regression


```python
def coef(data_group):
    '''
    We are going to use this function to model a regression of the change in temperature 
    against the years to find a coefficient over the yearly change in temperature.
    
    @param data_group: the group of data that you want to model your regression after
    
    return LR.coef_[0]: the coefficient of regression
    '''
    x = data_group[["Year"]] # 2 brackets because X should be a df
    y = data_group["Temp"]   # 1 bracket because y should be a series
    LR = LinearRegression()
    LR.fit(x, y)
    return LR.coef_[0]
```

We are going to incorporate the coefficients with the original queried dataframe in a function that will soon create a nice pretty picture... Just follow my comments and I'll explain.


```python
def temperature_coefficient_plot(country, year_begin, year_end, month, min_obs, **kwargs):
    '''
    This function will create an interactive geographic scatter mapbox, 
    constructed using Plotly Express, with a point for each station, 
    such that the color of the point reflects an estimate of the yearly 
    change in temperature during the specified month and time period at that station
    
    @param country: a string giving the name of a country for which data should be returned
    @param year_begin and year_end: two integers giving the earliest and latest years for 
                                    which should be returned
    @param month: an integer giving the month of the year for which should be returned
    @param min_obs: an integer stating the minimum required number of years of data 
                    for any given station
    @param **kwargs: additional keyword arguments passed to px.scatter_mapbox()                
    
    return a plotly express interactive mapbox of user specified variables. 
    '''
    
    #creates a queried database of the specified variables (so computer mustn't parse through all)
    queri = query_climate_database(country, year_begin, year_end, month)
    
    #will create a new dataframe will the coeficcients of each station over the years
    coefs = queri.groupby(["NAME", "Month"]).apply(coef)
    coefs = coefs.reset_index()
    coefs = coefs.rename(columns = {0  : "Estimated Yearly Increase (℃)"})
    coefs["Estimated Yearly Increase (℃)"] = round(coefs["Estimated Yearly Increase (℃)"], 5)
    
    #merges the two together to be easily plottable
    queri = pd.merge(queri, coefs, on=['NAME','Month'])
    
    #makes sure that Only data for stations with at least min_obs years worth of data 
    #in the specified month should be plotted; the others should be filtered out.
    queri = queri.groupby('NAME').filter(lambda x: len(x) >= min_obs)
    
    #a dictionary to easily change title based on user inputted variables
    monthDict = {1:'January',
                 2:'February',
                 3:'March',
                 4:'April',
                 5:'May',
                 6:'June',
                 7:'July',
                 8:'August',
                 9:'September',
                10:'October',
                11:'November',
                12:'December'}
    
    #title prompt for the plot    
    title = "Estimates of yearly increase in temperature in {} for stations in {}, years {} - {}"
    #updating with user inputted variables
    title = title.format(monthDict[month], country, year_begin, year_end)
    
    #plot
    return px.scatter_mapbox(queri, 
                            lon="LONGITUDE",
                            lat="LATITUDE",
                            color="Estimated Yearly Increase (℃)", # which column to use to set the color of markers
                            hover_name="NAME", # column added to hover information
                            title = title,
                            **kwargs)
```

Now if we did it right it should work...


```python
color_map = px.colors.diverging.RdGy_r # choose a colormap

fig = temperature_coefficient_plot("India", 1980, 2020, 1, 
                                   min_obs = 50,
                                   zoom = 2,
                                   mapbox_style="carto-positron",
                                   color_continuous_scale=color_map)

fig.show()
```
{% include temperature_coefficient_plot.html %}

Look at that! Our own interactive map!!

## §4. Create Two More Interesting Figures

First we can see if there's any correlations between any of the variables by doing a large matrix grid of plots.


```python
def scatter_matrix_plot(country, year_begin, year_end, month, min_obs, **kwargs):
    '''
    This function will create a large matrix grid of plots that will give an overview 
    of the different variables and how they look like when compared to each other. 
    
    @param country: a string giving the name of a country for which data should be returned
    @param year_begin and year_end: two integers giving the earliest and latest years for 
                                    which should be returned
    @param month: an integer giving the month of the year for which should be returned
    @param min_obs: an integer stating the minimum required number of years of data 
                    for any given station
    @param **kwargs: additional keyword arguments passed to px.scatter_matrix()                
    
    return a plotly express scattter maxtrix of user specified variables. 
    '''
    
    #creates a queried database of the specified variables 
    #(so computer mustn't parse through all)
    queri = query_climate_database(country, year_begin, year_end, month)
    
    #will create a new dataframe will the coeficcients of each station over the years
    coefs = queri.groupby(["NAME", "Month"]).apply(coef)
    coefs = coefs.reset_index()
    coefs = coefs.rename(columns = {0  : "Estimated Yearly Increase (℃)"})
    coefs["Estimated Yearly Increase (℃)"] = round(coefs["Estimated Yearly Increase (℃)"], 5)
    coefs["EYI (℃)"] = coefs["Estimated Yearly Increase (℃)"]
    #merges the two together to be easily plottable
    queri = pd.merge(queri, coefs, on=['NAME','Month'])
    
    #makes sure that Only data for stations with at least min_obs years worth of data 
    #in the specified month should be plotted; the others should be filtered out.
    queri = queri.groupby('NAME').filter(lambda x: len(x) >= min_obs)
    
    #a dictionary to easily change title based on user inputted variables
    monthDict = {1:'January',
                 2:'February',
                 3:'March',
                 4:'April',
                 5:'May',
                 6:'June',
                 7:'July',
                 8:'August',
                 9:'September',
                10:'October',
                11:'November',
                12:'December'}
    
    #title prompt for the plot    
    title = "Estimates of yearly increase in temperature in {} for stations in {}, years {} - {}"
    #updating with user inputted variables
    title = title.format(monthDict[month], country, year_begin, year_end)
    
    #plot
    return px.scatter_matrix(queri,
                         dimensions = ["LONGITUDE", "LATITUDE", "EYI (℃)", "Year"],
                         color="Estimated Yearly Increase (℃)", # which column to use to set the color of markers
                         hover_name="NAME", # column added to hover information
                         title = title,
                         **kwargs)
```


```python
fig = scatter_matrix_plot("Chile", 2000, 2021, 1, min_obs = 10)

fig.show()
```
{% include scatter_matrix_plot.html %}

It looks like there may be a slight negative correlation between longitude and EYI, so I'd like to invesitgate that further...

I would like to see whether the latitude in certain climates are more affects are more prone to changes in temperature over the years. ( ie are those stations closer to the equator more likely to have a higher coefficient and vice versa)


```python
def latitude_coefficient_plot(country, year_begin, year_end, month, min_obs, **kwargs):
    '''
    This function will create an scatter plot complete with a trendline to compare
    the Estimated Yearly Increase vs the latitude of each station.
    
    @param country: a string giving the name of a country for which data should be returned
    @param year_begin and year_end: two integers giving the earliest and latest years for 
                                    which should be returned
    @param month: an integer giving the month of the year for which should be returned
    @param min_obs: an integer stating the minimum required number of years of data 
                    for any given station
    @param **kwargs: additional keyword arguments passed to px.scatter            
    
    return a plotly express scatterplot of user specified variables. 
    '''
    
    #creates a queried database of the specified variables (so computer mustn't parse through all)
    queri = query_climate_database(country, year_begin, year_end, month)
    
    #will create a new dataframe will the coeficcients of each station over the years
    coefs = queri.groupby(["NAME", "Month"]).apply(coef)
    coefs = coefs.reset_index()
    coefs = coefs.rename(columns = {0  : "Estimated Yearly Increase (℃)"})
    coefs["Estimated Yearly Increase (℃)"] = round(coefs["Estimated Yearly Increase (℃)"], 5)
    
    #merges the two together to be easily plottable
    queri = pd.merge(queri, coefs, on=['NAME','Month'])
    
    #makes sure that Only data for stations with at least min_obs years worth of data 
    #in the specified month should be plotted; the others should be filtered out.
    queri = queri.groupby('NAME').filter(lambda x: len(x) >= min_obs)
    
    #a dictionary to easily change title based on user inputted variables
    monthDict = {1:'January',
                 2:'February',
                 3:'March',
                 4:'April',
                 5:'May',
                 6:'June',
                 7:'July',
                 8:'August',
                 9:'September',
                10:'October',
                11:'November',
                12:'December'}
    
    #title prompt for the plot    
    title = "Estimates of yearly increase in temperature in {} for stations in {}, years {} - {} by Latitude"
    #updating with user inputted variables
    title = title.format(monthDict[month], country, year_begin, year_end)

    #plot
    return px.scatter(queri,
                      x = "LATITUDE",
                      y = "Estimated Yearly Increase (℃)",
                      hover_name="NAME", # column added to hover information
                      hover_data = ["Year"],
                      title = title,
                      trendline = "ols",
                      **kwargs)
```


```python
fig = latitude_coefficient_plot("Chile", 2000, 2021, 1, min_obs = 10)

fig.show()
```
{% include latitude_coefficient_plot.html %}

Well this did not go how I expected. You can hover over the trendline to get some quick stats. I am quite suprised at the R-value. I guess looking at the graph however, it is quite obvious why it is so low. However, an R-Value of .08, while proof of no correlation, IS better than 0. So maybe we learned that maybe... MAYBE as you get closer to the equator, there is less of an estimated yearly increase, but we would need much more data and more correlation to conclude that.
