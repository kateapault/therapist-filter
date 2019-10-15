import pandas
import requests
from bs4 import BeautifulSoup

zipcodes = []
for i in range(0,100000):
    if len(str(i)) < 5:
        zipcodes.append(str(i).zfill(5))
    else:
        zipcodes.append(str(i))

validzipcodes = []
vzc = []
i = 0
j = 1

for code in zipcodes[0:1000]:
    url = 'https://www.geonames.org/postalcode-search.html?q='+ code + '&country=US'
    mainpagehtml = requests.get(url)
    if 'No rows found' not in BeautifulSoup(mainpagehtml.content,'html.parser').body.get_text():
        vzc.append(code)
    if j % 100 == 0: print(str(j) + " cycles complete")
    j += 1
validzipcodes += vzc
vzc = []
i += 1


validzipcodes.to_csv('validzipcodes.csv',',')
