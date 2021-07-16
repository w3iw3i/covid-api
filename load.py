# Get data
# ================

import pandas as pd
import numpy as np

# Read in dataset
# ======
confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
recovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
# confirmed_us = pd.read_csv('../data/time_series_covid19_confirmed_us.csv')
# deaths_us = pd.read_csv('../data/time_series_covid19_deaths_us.csv')

# extract date columns
dates = confirmed.columns[4:]

# melt dataframes into longer format
# ==================================
confirmed_long = confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
                            value_vars=dates, var_name='Date', value_name='Confirmed')

deaths_long = deaths.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
                            value_vars=dates, var_name='Date', value_name='Deaths')                         

recovered_long = recovered.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
                            value_vars=dates, var_name='Date', value_name='Recovered')
# recovered_long = recovered_long[recovered_long['Country_Region']!='Canada']

# confirmed_us_long = confirmed_us.melt(id_vars=['Province_State', 'Country_Region', 'Lat', 'Long_'], 
#                             value_vars=dates, var_name='Date', value_name='Confirmed')
# confirmed_us_long.rename(columns={'Long_' : 'Long'}, inplace=True)

# deaths_us_long = deaths_us.melt(id_vars=['Province_State', 'Country_Region', 'Lat', 'Long_'], 
#                             value_vars=dates, var_name='Date', value_name='Deaths')  
# deaths_us_long.rename(columns={'Long_' : 'Long'}, inplace=True)                                                                                   


# merge dataframes
# ================
master_table = pd.merge(left=confirmed_long, right=deaths_long, how='left',
                      on=['Province/State', 'Country/Region', 'Date', 'Lat', 'Long'])
master_table = pd.merge(left=master_table, right=recovered_long, how='left',
                      on=['Province/State', 'Country/Region', 'Date', 'Lat', 'Long'])
master_table.rename(columns={'Province/State' : 'Province_State', 'Country/Region' : 'Country_Region'}, inplace=True)


# Convert to proper date format
master_table['Date'] = pd.to_datetime(master_table['Date'])

# fill na with 0
master_table['Recovered'] = master_table['Recovered'].fillna(0)
# master_table['Lat'] = master_table['Lat'].fillna(0)
# master_table['Long'] = master_table['Long'].fillna(0)

# convert to int datatype
master_table['Recovered'] = master_table['Recovered'].astype('int')

# Active Case = confirmed - deaths - recovered
master_table['Active'] = master_table['Confirmed'] - master_table['Deaths'] - master_table['Recovered']

# fixing Country names
# ====================

# renaming countries, regions, provinces
master_table['Country_Region'] = master_table['Country_Region'].replace('Korea, South', 'South Korea')

# Greenland
master_table.loc[master_table['Province_State'] =='Greenland', 'Country_Region'] = 'Greenland'

# Mainland china to China
master_table['Country_Region'] = master_table['Country_Region'].replace('Mainland China', 'China')

# Taiwan* to Taiwan
master_table['Country_Region'] = master_table['Country_Region'].replace('Taiwan*', 'Taiwan')


# filling missing values 
# ======================
# fill missing province/state value with ''
master_table[['Province_State']] = master_table[['Province_State']].fillna('')

# fill missing numerical values with 0
cols = ['Confirmed', 'Deaths', 'Recovered', 'Active']
master_table[cols] = master_table[cols].fillna(0)

# Derive day wise New confirmed, New deaths and New recovered columns
sorted_table = master_table.sort_values(['Country_Region', 'Province_State', 'Date'])
diff_table = sorted_table.iloc[:, 5:8].diff().fillna(0)
mask_country = sorted_table['Country_Region'] != sorted_table['Country_Region'].shift(1)
mask_province = sorted_table['Province_State'] != sorted_table['Province_State'].shift(1)

# Updating boundary first record for each country or province
diff_table.loc[mask_country, 'Confirmed'] = sorted_table.loc[mask_country, 'Confirmed']
diff_table.loc[mask_country, 'Deaths'] = sorted_table.loc[mask_country, 'Deaths']
diff_table.loc[mask_country, 'Recovered'] = sorted_table.loc[mask_country, 'Recovered']
diff_table.loc[mask_province, 'Confirmed'] = sorted_table.loc[mask_province, 'Confirmed']
diff_table.loc[mask_province, 'Deaths'] = sorted_table.loc[mask_province, 'Deaths']
diff_table.loc[mask_province, 'Recovered'] = sorted_table.loc[mask_province, 'Recovered']
diff_table.rename(columns={'Confirmed' : 'New_Confirmed', 'Deaths' : 'New_Deaths', 'Recovered' : 'New_Recovered'}, inplace=True)
final_table = sorted_table.join(diff_table)

# convert to int datatype
final_table['New_Confirmed'] = final_table['New_Confirmed'].astype('int')
final_table['New_Deaths'] = final_table['New_Deaths'].astype('int')
final_table['New_Recovered'] = final_table['New_Recovered'].astype('int')

# Export to csv
final_table.to_csv('./data/master.csv', index=False)

# Export list of countries
country_list = pd.DataFrame(data=final_table['Country_Region'].unique(), columns=['Country'])
country_list.to_csv('./data/country.csv', index=False)