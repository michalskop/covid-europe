# Europe

Data for a detailed map of covid cases in central Europe

Published here: https://www.seznamzpravy.cz/clanek/aktualni-mapa-stredni-evropy-hranice-vykresluje-koronavirus-144415

## Germany

source: https://github.com/jgehrcke/covid-19-germany-gae

map: https://github.com/jgehrcke/covid-19-germany-gae/tree/master/geodata
alternative: https://osm-boundaries.com/Map 

data: https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/more-data/latest-aggregate.csv
(always updated)

1. join few ares in the map
https://gis.stackexchange.com/questions/233489/merging-attribute-and-geometric-features-in-qgis

2. upload to Flourish + remove and rename columns, sort by map_code

3. run germany.py

## Austria
source: https://www.data.gv.at/katalog/dataset/4b71eb3d-7d55-4967-b80d-91a3f220b60c

data: https://covid19-dashboard.ages.at/data/CovidFaelle_Timeline_GKZ.csv

map: https://github.com/ginseng666/GeoJSON-TopoJSON-Austria/blob/master/2021/simplified-95/bezirke_95_geo.json

1. upload to flourish + reorder and rename and remove columns + sortby map_name + remove Wien bezirks rows

2.run austria.py

## Poland
source: https://www.gov.pl/web/koronawirus/wykaz-zarazen-koronawirusem-sars-cov-2

data: https://www.arcgis.com/sharing/rest/content/items/6ff45d6b5b224632a672e764e04e8394/data

map: https://gis-support.pl/baza-wiedzy-2/dane-do-pobrania/granice-administracyjne/

0. create geojson from shp

0. 
```
geo2topo pl_counties_original.geo.json > pl_counties_original.topo.json
toposimplify -P 0.01 -f < pl_counties_original.topo.json > pl_counties-topo.json
topo2geo < pl_counties-topo.json pl_counties_original.geo=pl_counties.geo.json
```

1. upload to flourish + reorder and rename columns + sortby name + remove Wien bezirks rows

## Slovakia
source:

data: https://github.com/Institut-Zdravotnych-Analyz/covid19-data/raw/main/PCR_Tests/OpenData_Slovakia_Covid_PCRTests_District.csv

data2: https://github.com/Institut-Zdravotnych-Analyz/covid19-data/blob/main/AG_Tests/OpenData_Slovakia_Covid_AgTests_District.csv

demography: http://statdat.statistics.sk/cognosext/cgi-bin/cognos.cgi?b_action=cognosViewer&ui.action=run&ui.object=storeID%28%22i362DCE4D88EC4E13A9EE8526B286D18B%22%29&ui.name=Po%C4%8Det%20obyvate%C4%BEov%20pod%C4%BEa%20pohlavia%20-%20SR%2C%20oblasti%2C%20kraje%2C%20okresy%2C%20mesto%2C%20vidiek%20%28ro%C4%8Dne%29%20%5Bom7102rr%5D&run.outputFormat=&run.prompt=true&cv.header=false&ui.backURL=%2Fcognosext%2Fcps4%2Fportlets%2Fcommon%2Fclose.html&run.outputLocale=sk

0. 
```
geo2topo sk_counties_original.geo.json > sk_counties_original.topo.json
toposimplify -P 0.05 -f < sk_counties_original.topo.json > sk_counties-topo.json
topo2geo < sk_counties-topo.json tracts=sk_counties.geo.json
```

1. upload to flourish + reorder and rename columns + sortby map_code + remove Wien bezirks rows

2. slovakia.py

## Czechia

data: 

map: https://data.gov.cz/attachments/%C4%8Dl%C3%A1nky/kartogram-choropleth/data/okresy-simple.json

## Hungary

Source: http://pandemia.hu/koronavirus-megyeterkep-magyarorszagi-adatok-megyei-bontasban/

Map: https://gisco-services.ec.europa.eu/distribution/v2/nuts/download/ref-nuts-2021-01m.geojson.zip

Demography: https://hu.wikipedia.org/wiki/Magyarorsz%C3%A1g_megy%C3%A9i 

0. filter HU map in QGIS

1. manually `prepare hu_population.csv`

2. `hungary.py`
