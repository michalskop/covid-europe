"""Prepare data for Slovakia."""

import gspread
import pandas as pd 
import numpy as np

# read data
url = "https://github.com/Institut-Zdravotnych-Analyz/covid19-data/raw/main/PCR_Tests/OpenData_Slovakia_Covid_PCRTests_District.csv"

data = pd.read_csv(url, sep=';')

# filter last date only
last_time = data.tail(1)['Date'].values[0]
last_times = sorted(data['Date'].unique())[-7:]

data7 = data[data['Date'].isin(last_times)]
data = data[data['Date'] == last_time]

data7 = data7[~data7['District_code'].isin(['SK000', '?', 'SKZZZZ'])]
data = data[~data['District_code'].isin(['SK000', '?', 'SKZZZZ'])]

data7 = data7.reset_index()
data = data.reset_index()

pt = pd.pivot_table(data7, values='PCR_Pos', index='District', aggfunc=np.sum)
pt.reset_index(inplace=True)

data = data.sort_values('District')
pt = pt.sort_values('District')

# read demography
# http://statdat.statistics.sk/cognosext/cgi-bin/cognos.cgi?b_action=cognosViewer&ui.action=run&ui.object=storeID%28%22i362DCE4D88EC4E13A9EE8526B286D18B%22%29&ui.name=Po%C4%8Det%20obyvate%C4%BEov%20pod%C4%BEa%20pohlavia%20-%20SR%2C%20oblasti%2C%20kraje%2C%20okresy%2C%20mesto%2C%20vidiek%20%28ro%C4%8Dne%29%20%5Bom7102rr%5D&run.outputFormat=&run.prompt=true&cv.header=false&ui.backURL=%2Fcognosext%2Fcps4%2Fportlets%2Fcommon%2Fclose.html&run.outputLocale=sk
f = "./sk_population.csv"
demo = pd.read_csv(f)
demo = demo.sort_values('name')

# join
data = data.merge(demo, how='left', left_on='District', right_on='name')
data = data.merge(pt, how='left', left_on='District', right_on='District')

data7[data7['District'] == 'Okres Snina']

# create new dataframe
header = ['id', 'code', 'name', 'population', 'prevalence', 'incidence_7', 'prevalence_100k', 'incidence_7_100k', 'country']

df = pd.DataFrame(columns=header)

df['code'] = data['District_code']
df['name'] = data['District'].str.replace('Okres ', '')
df['id'] = data['District_code'].str.replace('SK', 'SK-')
df['population'] = data['population']
df['incidence_7'] = data['PCR_Pos_y']
df['incidence_7_100k'] = df['incidence_7'] / df['population'] * 100000
df['country'] = 'Slovakia'

df = df.sort_values('id')

df = df.fillna('')

# write to GSheet
if len(sys.argv) > 1:
    gc = gspread.service_account(sys.argv[1])
else:
    gc = gspread.service_account()
sheetkey = "1DRDJvFQstk-4dVajSOzUupaLcWMVEqjajyzHh8gfbdQ"

sh = gc.open_by_key(sheetkey)
ws = sh.worksheet('Slovakia')

ws.update([df.columns.values.tolist()] + df.values.tolist())

# save to csv
df.to_csv("data/slovakia.csv")