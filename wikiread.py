# wikiscraper
# author: Timur Bazhirov
# last edited: Nov 30, 2012
#
# This function searches if a particular named article is present on Wikipedia
# then it checks if the passed latitude is close to the found article's latitude 
# and outputs a python dictionary with a first paragraph from Wikipedia and a photo url

import urllib, urllib2 
from BeautifulSoup import BeautifulSoup
import lxml.html
from conversion import conversion

# GPS precision
GPS_FLOAT_PRECISION = 1e10-4

# What is being returned in case the article with a particular name is not found 
NODATA = dict([('desc',"No description available"),('pic',"N/A")])

def wikiread(string, latit):

# preliminary section
    article = string
    article = urllib.quote(article)

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

# posting http request and reading the data
    try:
        resource = opener.open("http://en.wikipedia.org/wiki/" + article)
    except urllib2.URLError:
        return NODATA
        pass

    data = resource.read()
    resource.close()
    soup = BeautifulSoup(data)

# parsing the data with BeautifulSoup    
    wiki_first_paragraph = soup.find('div',id="bodyContent").p 

    try:
        wiki_latitude = conversion(soup.find('span',attrs={"class":"latitude"}).renderContents())
    except AttributeError:
        wiki_latitude = "N/A"
        pass

    try:
        wiki_longitude = conversion(soup.find('span',attrs={"class":"longitude"}).renderContents())
    except AttributeError:
        wiki_longitude = "N/A"
        pass

    try:
        wiki_pic = soup.find('img')['src']
    except AttributeError:
        wiki_pic = "N/A"
        pass

# checking if the wiki_latitude is close to the initially given one
    b = "N/A"
    try:
        diff = float(abs(wiki_latitude) - abs(latit))
        if diff < GPS_FLOAT_PRECISION:
           b = wiki_pic
    except TypeError:
        return NODATA
        pass


    text = lxml.html.fromstring(str(wiki_first_paragraph))
    a = text.text_content()
 
 # forming python dict for output    
    out = dict([('desc',a),('pic',b)])

    return out
