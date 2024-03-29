"""Prepare data for Austria."""

import gspread
import io
import pandas as pd
import requests
import urllib3
import sys

# read data
url = "http://covid19-dashboard.ages.at/data/CovidFaelle_Timeline_GKZ.csv"

# disable verification https://stackoverflow.com/a/41041028/1666623
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

r = requests.get(url, verify=False)

# read requests https://stackoverflow.com/a/39213616/1666623
data = pd.read_csv(io.StringIO(r.text), sep=';')

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
if len(sys.argv) > 1:
    gc = gspread.service_account(sys.argv[1])
else:
    gc = gspread.service_account()
sheetkey = "1DRDJvFQstk-4dVajSOzUupaLcWMVEqjajyzHh8gfbdQ"

# Cibulka show
# gc = gspread.service_account()
# sheetkey = "1DRDJvFQstk-4dVajSOzUupaLcWMVEqjajyzHh8gfbdQ"

sh = gc.open_by_key(sheetkey)
ws = sh.worksheet('Austria')

ws.update([df.columns.values.tolist()] + df.values.tolist())

# save to csv
df.to_csv("data/austria.csv")