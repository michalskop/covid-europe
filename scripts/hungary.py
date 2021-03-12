"""Prepare data for Hungary."""

import csv
import gspread
import pandas as pd
import re
from requests_html import HTMLSession
import sys

# create new dataframe
header = ['id', 'code', 'name', 'population', 'prevalence', 'incidence_7', 'prevalence_100k', 'incidence_7_100k', 'country', 'date']

df = pd.DataFrame(columns=header)

# read population
f = "scripts/hu_population.csv"
population = pd.read_csv(f)
population = population.sort_values('name')

# get data
session = HTMLSession()

url = "http://pandemia.hu/koronavirus-megyeterkep-magyarorszagi-adatok-megyei-bontasban/"

r = session.get(url)

# date
t = r.html.find('p[style="text-align:center"]', first=True).text
pattern = "[0-9]{4}.[0-9]{2}.[0-9]{2}"
date = re.findall(pattern, t)[0].replace('.', '-')

# values
table = r.html.find('table', first=True)
trs = table.find('tr')
del trs[0]

for tr in trs:
    tds = tr.find('td')
    it = {
        'name': tds[0].text,
        'incidence_7': tds[3].text.replace('+',''),
        'date': date
    }
    df = df.append(it, ignore_index=True)

df = df.sort_values('name')

# join population (sorted by name, original sort)
df['id'] = population['code'].str.replace('HU', 'HU-')
df['code'] = population['code']
df['population'] = population['population']
df['incidence_7_100k'] = df['incidence_7'].astype(int) / df['population'] * 100000
df['country'] = 'Hungary'

df = df.fillna('')

# final sort by id
df = df.sort_values('id')

# write to GSheet
if len(sys.argv) > 1:
    gc = gspread.service_account(sys.argv[1])
else:
    gc = gspread.service_account()
sheetkey = "1DRDJvFQstk-4dVajSOzUupaLcWMVEqjajyzHh8gfbdQ"

sh = gc.open_by_key(sheetkey)
ws = sh.worksheet('Hungary')

ws.update([df.columns.values.tolist()] + df.values.tolist())

# save to csv
df.to_csv("data/hungary.csv")