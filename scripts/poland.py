"""Prepare data for Poland."""

import gspread
import io
import numpy as np
import pandas as pd
import requests
import sys
import zipfile


# read data
url = "https://arcgis.com/sharing/rest/content/items/e16df1fa98c2452783ec10b0aea4b341/data"

# get file names
r = requests.get(url, stream=True)
z = zipfile.ZipFile(io.BytesIO(r.content))
fnames = z.namelist()[-8:-1]    # remove readme.txt and last date

i = 0
for fname in fnames:
    if i == 0:
        data7 = pd.read_table(z.open(fname), encoding="cp1250", sep=";")
        data7 = data7[~data7['powiat_miasto'].isin(['Cały kraj'])]
    else:
        data = pd.read_table(z.open(fname), encoding="cp1250", sep=";")
        data = data[~data['powiat_miasto'].isin(['Cały kraj'])]
        data7 = pd.concat([data7, data]) 
    i += 1

data = data.sort_values('teryt')

# sum 7 days
# data7.to_csv('pl_temp.csv')
pt = pd.pivot_table(data7, values=['liczba_przypadkow', 'liczba_na_10_tys_mieszkancow'], index=['powiat_miasto', 'teryt'], aggfunc=np.sum)
pt = pt.sort_values('teryt')
pt.reset_index(inplace=True)
# pt.to_csv('pl_temp2.csv')

# population - once:
# population = pd.DataFrame()
# population['name'] = pt['powiat_miasto']
# population['code'] = pt['teryt']
# population['population'] = (round(pt['liczba_przypadkow'] / pt['liczba_na_10_tys_mieszkancow'] * 10000)).astype(int)
# population = population.sort_values('code')
# population.to_csv('pl_population.csv')
population = pd.read_csv("scripts/pl_population.csv").reset_index()

data = data.merge(population, how="left", left_on="teryt", right_on="code")
data7 = data7.merge(population, how="left", left_on="teryt", right_on="code")

data = data.sort_values('teryt')
# data.to_csv('pl_temp3.csv')

# create new dataframe
header = ['id', 'code', 'name', 'population', 'prevalence', 'incidence_7', 'prevalence_100k', 'incidence_7_100k', 'country']

df = pd.DataFrame(columns=header)

df['name'] = data['powiat_miasto']
df['id'] = 'PL-' + data['teryt']
df['code'] = data['teryt']
df['population'] = data['population']
df['incidence_7'] = pt['liczba_przypadkow']
df['incidence_7_100k'] = df['incidence_7'] / df['population'] * 100000
df['country'] = 'Poland'

df = df.fillna('')
df = df.sort_values('code')

# df.to_csv('pl_temp4.csv')

# write to GSheet
if len(sys.argv) > 1:
    gc = gspread.service_account(sys.argv[1])
else:
    gc = gspread.service_account()
sheetkey = "1DRDJvFQstk-4dVajSOzUupaLcWMVEqjajyzHh8gfbdQ"

sh = gc.open_by_key(sheetkey)
ws = sh.worksheet('Poland')

ws.update([df.columns.values.tolist()] + df.values.tolist())

# save to csv
df.to_csv("data/poland.csv")