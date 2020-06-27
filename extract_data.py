import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import random


df = pd.read_csv('owid-covid-data.csv')
country_name = sorted(set(df['location']))
country_slice = {}
date_begin = datetime.strptime('2019-12-31', '%Y-%m-%d')
# resample date and set date to index => fill all data, to balance countries' data.

for country in country_name:
    if df[df.location == country].date.iloc[0] == '2019-12-31':
        country_slice[country] = df[df.location == country]
        # reformat_data(country)
        country_slice[country].set_index(pd.to_datetime(country_slice[country].date), inplace=True)
        country_slice[country] = country_slice[country].resample('D').sum().fillna('0')
        # fillna for col
        for col in country_slice[country].columns:
            for i in range(1, len(country_slice[country][col])):
                if country_slice[country][col].iloc[i - 1] != 0.0 and country_slice[country][col].iloc[i] == 0.0:
                    country_slice[country][col].iloc[i] = country_slice[country][col].iloc[i - 1]
    else:
        country_slice[country] = df[df.location == country].append({'date':'2019-12-31'}, ignore_index=True)
        # reformat_data(country)
        country_slice[country].set_index(pd.to_datetime(country_slice[country].date), inplace=True)
        country_slice[country] = country_slice[country].resample('D').sum().fillna('0')
        # fillna for col
        for col in country_slice[country].columns:
            for i in range(1, len(country_slice[country][col])):
                if country_slice[country][col].iloc[i - 1] != 0.0 and country_slice[country][col].iloc[i] == 0.0:
                    country_slice[country][col].iloc[i] = country_slice[country][col].iloc[i - 1]

random_country = [random.choice(country_name) for x in range(5)]
data_plot = np.array([country_slice[country].total_cases for country in random_country]).transpose()
list_date = list(country_slice['Vietnam'].index.astype('str'))
# plt.xticks([0,50,100,150,177])
# plt.plot(list_date, data_plot)
# plt.legend(random_country)

# testing
# make new db vs col = ['country_name', 'continent', date]
lst_country_test = country_name
row_list = []

for country in lst_country_test:
    dct_data = {}
    dct_data['Country'] = country
    dct_data['Continent'] = list(df[df['location'] == country].continent)[0]
    list_total_cases = list(np.array(country_slice[country].total_cases).transpose())
    dct_data.update(dict(zip(list_date, list_total_cases)))
    row_list.append(dct_data)

col = ['Country', 'Continent'] + list_date
df_out = pd.DataFrame(columns=col)

df_out = df_out.append(row_list, ignore_index = True)
df_out.to_csv('total_cases_per_country.csv')