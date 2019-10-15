'''
returns list of dicts with info for therapists in specified city and state
name, jobTitle, addressLocality(=city), addressRegion(=state),postalcode
offices/groups have no jobTitle attribute
(from first page of results from PsychologyToday.com)
'''

from bs4 import BeautifulSoup
import requests

def getPsychData(city, state):

    url = 'https://www.psychologytoday.com/us/therapists/' + state.lower() + '/' + city.lower()
    # header added after running requests.get(url) by itself returned a 403 status code
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15'}
    mainpagehtml = requests.get(url,headers=headers)

    try:
        # turn html into BeautifulSoup object
        soup = BeautifulSoup(mainpagehtml.content,'html.parser')
        mainpage = soup.body

        # site uses this div class for therapist listings in results. ResultSet object.
        therapist_results = soup.find_all('div',{'class': 'result-row normal-result row'})

        # therapist info is in span tags; itemprop attribute gives label for info (eg job title, etc)
        spans = therapist_results[0].find_all('span')
        spanitemprops = []
        for span in spans:
            if span.get('itemprop'): spanitemprops.append(span.get('itemprop'))

        therapists = []
        for i in range(0,len(therapist_results)):
            propertieslist = therapist_results[i]('span',{'itemprop':spanitemprops})
            therapist_info = {}
            for prop in propertieslist:
                if prop.get_text():
        # lots of buttons/subtags that have '\n\n\n' as get_text(), some itemprop attributes (eg city) repeat within listings
                    if '\n' in prop.get_text(): pass
                    elif prop.get('itemprop') in therapist_info.keys(): pass
                    else: therapist_info[prop.get('itemprop')] = prop.get_text()
            therapists.append(therapist_info)
        return therapists

    except Exception as ex:
        print(ex)




# sites to scrape for therapists:
# psychology today
# goodtherapy.org
# networktherapy.com
