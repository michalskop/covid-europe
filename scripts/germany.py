"""Prepare data for Germany."""

import gspread
import pandas as pd 

url = "https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/more-data/latest-aggregate.csv"

data = pd.read_csv(url, header=1)

# remove Berlin parts
remove_berlin = data[ (data['ags'] >= 11001) & (data['ags'] <= 11012) ].index
data.drop(remove_berlin , inplace=True)

# create new dataframe
header = ['id', 'code', 'name', 'population', 'prevalence', 'incidence_7', 'prevalence_100k', 'incidence_7_100k', 'country', 'state']

df = pd.DataFrame(columns=header)

def _n4to5(n):
    if n < 10000:
        return "0" + str(n)
    else:
        return str(n)

df['name'] = data['county_name']
df['id'] = 'DE-' + data['ags'].apply(_n4to5)
df['code'] = data['ags'].apply(_n4to5)
df['population'] = data['population']
df['state'] = data['state']
df['incidence_7'] = data['rki_cases_7di']
df['incidence_7_100k'] = df['incidence_7'] / df['population'] * 100000
df['country'] = 'Germany'

df = df.fillna('')

# write to GSheet
gc = gspread.service_account()
sheetkey = "1DRDJvFQstk-4dVajSOzUupaLcWMVEqjajyzHh8gfbdQ"

sh = gc.open_by_key(sheetkey)
ws = sh.worksheet('Germany')

ws.update([df.columns.values.tolist()] + df.values.tolist())

# save to csv
df.to_csv("../data/germany.csv")