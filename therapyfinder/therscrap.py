from bs4 import BeautifulSoup
import requests

#input user parameters eventually

# get results listing of therapists in BK
# this is only the first page right now
def getPsychData(city, state, bool):
    from bs4 import BeautifulSoup
    import requests
    urltrue = 'https://www.psychologytoday.com/us/therapists/' + state + '/' + 'city'
    urlfalse = 'https://www.psychologytoday.com/us/therapists/ny/brooklyn'
    # header added after running requests.get(url) by itself returned a 403 status code
    if bool:
        url = urltrue
    else: url = urlfalse
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15'}
    mainpagehtml = requests.get(url,headers=headers)
    # make sure page is available
    try:
        # turn html into beautifulsoup object
        soup = BeautifulSoup(mainpagehtml.content,'html.parser')
        mainpage = soup.body
        # filter to just get therapist results. without [0] results is a ResultSet, with [0] it's a Tag
        th_results = soup.find_all('div',{'class': 'result-row normal-result row'})

        # span is the tag that contains name, job title, address, etc.
        # Using this for now (eventually will pull profile link and get info from there; this is just to start)
        # get everything with a span tag
        th_infolist = []

        for result in th_results:
            th_spans = th_results.find_all('span')
            # get list of the properties for each span tag
            spanitemprops = []
            for line in th_spans:
                # if there's an 'itemprop' property, add it to the list spanitemprops
                if line.get('itemprop'): spanitemprops.append(line.get('itemprop'))

            infodict = {}
            # list just unique properties
            spanitemprops_u = set(spanitemprops)
            # search through t and grab things with those itemprop values ; this can take a list of strings and search for
            # itemprops that match any string in the list. This produces a list of tags with those matching itemprops
            propertieslist = th_results('span',{'itemprop':spanitemprops_u})

            # go through list of matching tags. for each tag, add the itemprop value as dict key and tag's string as dict value
            for each in propertieslist:
                if each.get_text():
                    infodict[each.get('itemprop')] = each.get_text()
            print(infodict)
            th_infolist.append(infodict)

        return th_infolist
    except:
        print('something went wrong')


getPsychData('Brooklyn','NY',False)


# sites to scrape for therapists:
# psychology today
# goodtherapy.org
# networktherapy.com
