#!/usr/bin/env python3

import csv
import urllib.request
from bs4 import BeautifulSoup

stations_url = 'https://network.satnogs.org/stations/'
csv_file_path = 'stations.csv'

print('Requesting', stations_url)
stations_page = urllib.request.urlopen(stations_url).read().decode('utf8')

print('Parsing')
soup = BeautifulSoup(stations_page, 'html.parser')


# with open("index.html") as fp:
    # soup = BeautifulSoup(fp, 'html.parser')

active_stations = int(soup.find('div', attrs={'class': 'stations-totals'}).find('button').find('span').string)

rows = soup.find_all('tr', attrs={'class': 'station-row'})

print(active_stations,'active stations')
cur = 0;
with open(csv_file_path, 'w+') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['id','name','lat','lon','alt','antenna', 'frequency'])

    for tr in rows:
        if cur == active_stations:
            break

        tds = tr.find_all('td')

        ## id
        id = tds[0].find('span').string.strip()

        ## name
        name = tds[1].string.strip()

        ## Lat Lon
        latlon = tds[2].find('span')['title']
        comma = latlon.find(',')
        lat = latlon[:comma-1]
        lon = latlon[comma+2:-1]

        ## Alt
        alt_str = tds[2].find('span').string.strip()
        at_sym = alt_str.find('@')
        alt = alt_str[at_sym+1:-1]

        ## Antenna
        antennas = []
        for span in tds[5].find_all('span'):
            antennas.append(span.string.strip())
            antennas.append(span['title'])
        
        # print(','.join([id,name,lat,lon,alt,','.join(antennas)]))
        row = [id,name,lat,lon,alt]
        row.extend(antennas)
        writer.writerow(row)

        cur = cur + 1

print('wrote data to', csv_file_path)
