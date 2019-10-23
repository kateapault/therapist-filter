'''
This scrapes therapist information from psychologytoday.com
'''

from bs4 import BeautifulSoup
import requests
import csv

########################## SET UP FUNCTIONS ###################################
state = 'NY'
city = 'Brooklyn'

# returns therapist's profile page as ResultSet object given id number
def getPageFromID(idnum):
    url = 'https://www.psychologytoday.com/profile/' + idnum
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15'}
    mainpagehtml = requests.get(url,headers=headers)
    return BeautifulSoup(mainpagehtml.content,'html.parser')


def getInfo(pg,insdict):
    gotInfo = {}

    gotInfo['name'] = cleanString(pg.find('h1',{'itemprop':'name'}).get_text())
    gotInfo['phone'] = pg.find('div',{'class':'container main-content profile'}).find('a').get('href').split('+')[1]
    gotInfo['address'] = pg.find('div',{'class':"address-data"}).get('data-address-rank-1')
    gotInfo['title'] = simplifyTitle(pg.find('div',{'class':'modal-subtitle'}).get_text())
    gotInfo['remote'] = findRemote(pg)
    if findInsurance(pg,insdict) is None: gotInfo['insurance'] = insdict
    else: gotInfo['insurance'] = findInsurance(pg,insdict)

    return gotInfo


def simplifyTitle(string):
    if 'Psychiatrist' in string: return "Psychiatrist"
    elif 'Psychologist' in string: return 'Psychologist'
    elif 'Therapist' in string: return 'Therapist'
    elif 'Counselor' in string: return 'Therapist'


def cleanString(string):
    clean = ''
    for i in range(len(string)):
        if i == 0 and string[i] == ' ': pass
        elif string[i] == '\n': pass
        elif string[i] == ' ' and string[i-1] == ' ': pass
        elif string[i] == ' ' and string[i-1] == '\n': pass
        else: clean += string[i]
    return clean


def findRemote(pg):
# returns string; string may contain multiple methods of remote sessions eg online counseling and phone counseling
    if pg.find('div',{'class':'spec-list attributes-online-therapy'}):
        r = cleanString(pg.find('div',{'class':'spec-list attributes-online-therapy'}).get_text())
        return r.split('Video/Skype')[1]
    else:
        return 'Remote sessions not offered'


def findInsurance(pg,insdict):
    insurances = pg.find('div',{'class':'profile-finances details-section top-border'}).find('ul',{'class':'attribute-list copy-small'})
    if insurances is None:
        return insdict
    else:
        insurancestring = insurances.get_text()
        for company in insdict.keys():
            if company in insurancestring: insdict[company] = True
        return insdict

# get dict of insurance providers from csv file created earlier by pulling providers
# from available filters on mainpage. dict providers has insurance providers as keys
# and False for all values
with open('providerlist.csv',mode='r') as csvfile:
    fieldnames = insurancelist
    reader = csv.DictReader(csvfile)
    for row in reader:
        providers = row

################################################################
########################## SCRAPING ############################
################################################################

url = 'https://www.psychologytoday.com/us/therapists/' + state.lower() + '/' + city.lower()
# headers added after running requests.get(url) by itself returned a 403 status code
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15'}
mainpagehtml = requests.get(url,headers=headers)

# turn html into BeautifulSoup object
soup = BeautifulSoup(mainpagehtml.content,'html.parser')
mainpage = soup.body

# site uses this div class for therapist listings in results. ResultSet object.
therapist_results = soup.find_all('div',{'class': 'result-row normal-result row'})

# get site ids for therapists taking new patients
therapist_site_ids = []
for t in therapist_results:
    if t.get('data-new-clients')=='1':
        therapist_site_ids.append(t.get('data-profid'))

therapists = []
for siteID in therapist_site_ids:
    pggg = getPageFromID(siteID)
    therapists.append(getInfo(pggg,providers))
