"""Prepare data for Austria."""

import gspread
import pandas as pd 

# read data
url = "https://covid19-dashboard.ages.at/data/CovidFaelle_Timeline_GKZ.csv"

data = pd.read_csv(url, sep=';')

# filter last date only
last_time = data.tail(1)['Time'].values[0]
data = data[data['Time'] == last_time]
data = data.reset_index()

# create new dataframe
header = ['id', 'code', 'name', 'population', 'prevalence', 'incidence_7', 'prevalence_100k', 'incidence_7_100k', 'country']

df = pd.DataFrame(columns=header)

df['name'] = data['Bezirk']
df['id'] = 'AT-' + data['GKZ'].astype(str)
df['code'] = data['GKZ']
df['population'] = data['AnzEinwohner']
df['incidence_7'] = data['AnzahlFaelle7Tage']
df['incidence_7_100k'] = df['incidence_7'] / df['population'] * 100000
df['country'] = 'Austria'

df = df.fillna('')

# write to GSheet
gc = gspread.service_account()
sheetkey = "1DRDJvFQstk-4dVajSOzUupaLcWMVEqjajyzHh8gfbdQ"

sh = gc.open_by_key(sheetkey)
ws = sh.worksheet('Austria')

ws.update([df.columns.values.tolist()] + df.values.tolist())

# save to csv
df.to_csv("../data/austria.csv")