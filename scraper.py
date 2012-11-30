#!/usr/bin/env python

# wikiscraper
# author: Timur Bazhirov
# last edited: Nov 30, 2012
#
# The main script. Extracts wikipedia descriptions for all the objects in 
# the OpenStreetMaps XML file. First checks if description data is available
# from a local xml database  

import os
import sys
import json
import types
import re

from wikiread import wikiread
from osmparser import Parse
from externaldb import Caltour

#print "PLEASE MAKE SURE YOU'VE READ THE README THEN OPEN THE FILE AND COMMENT THIS LINE AND THE LINE PAST THIS ONE"
#sys.exit(0) # EXITS THE FIRST TIME



''' initiate necessary variables '''

# Data file name. MAKE SURE TO CHANGE for your run
XML_FILE_NAME = "./openstreetmap_example_data/example_OSM_UCB_campus.xml" 
EXTERNAL_XML_DB = "./external_database/places.xml"
EXT_DB_PICS_FLDR = "/Users/timur/Develop/guidedarea/Website_PlayFramework/public/pictures-ucb/"
EXT_DB_PICS_SRVR = "http://guidedarea.com/public/pictures-ucb/"
BLANK_IMAGE_URL = "https://encrypted-tbn1.google.com/images?q=tbn:ANd9GcSHSGrRjaWRTAlaHGrv-8TSwk8D17qmYFc1xfZiV2r8BTD_jGmhLA" 

# ID of the area all buildings belong to
higherid = "University of California, Berkeley"


''' script starts here '''

# Start Parsing OSM xml data
Data = Parse(XML_FILE_NAME,higherid)

# Read external database data - Caltour
Data1 = Caltour(EXTERNAL_XML_DB)

# number of matches found
Wiki = 0 
ext_db_matches = 0
piccounter = 0

# total # of objects in OSM xml file
counter = 1
# number of objects serialized into json
jsoncount = 0
Datajson = []

# Convert Data array to list and obtain descriptions/photos_urls

for elem in Data:

    counter += 1

    elem1 = dict(elem)

    # A hacky way to convert array entries into dict and get the arithmetic 
    # average latitude and longitude for the entry
    sumlat = 0
    sumlon = 0
    for elem2,elem3 in enumerate(elem1['points']):
      if isinstance(elem3, types.ListType): 
        elem1['points'][elem2] = dict(elem3)
        sumlat += float(elem3[0][1])
        sumlon += float(elem3[1][1])
    latitude = sumlat / len(elem1['points'])
    longitude = sumlon /len(elem1['points'])

    # That's how Parse.com type location wants to read the data
    location = {"__type":"GeoPoint", "latitude":round(latitude,6), "longitude":round(longitude, 6)}
    elem1['location'] = dict(location)

    # Checking for external database matches first
    matchflag = 0
    for item in Data1:
        item1 = dict(item)
        if item1['name'] == elem1['name']:
            elem1['description'] = item1['description'] 
            elem1['photo_link'] = "N/A"          
            ext_db_matches += 1
            matchflag = 1
            break
    
    # Checking for wikipedia matches now
    if matchflag == 0:
       try:
           wikiread_out = wikiread(elem1['name'], latitude)
           elem1['description'] = wikiread_out['desc']
           elem1['photo_link'] = "http:" + wikiread_out['pic']
           if elem1['description'] != "No description available": 
              Wiki += 1
       except KeyError:
           print "Oops!  That was a Unicode Warning..."
           elem1['photo_link'] = wikiread_out['pic']
           pass

    # Proper json formatting: getting rid of 's - TODO: make it work properly with \'s
    try:
        desc = elem1['description']
        desc = desc.replace('\\\'', '')
        elem1['description'] = desc
    except KeyError:
        pass

    # Check if external database has necessary pictures 
    # Below is a hacky way to check for the Caltour folders with pics
    stripname = elem1['name']
    stripname = stripname.replace(' ', '').lower()
    stripname = re.sub(r'\[.*?\]|\(.*?\)|\W', '',stripname) + ".jpg"
    #print "Stripped name is: ", stripname
    if os.path.isfile(EXT_DB_PICS_FLDR + stripname):
       elem1['photo_link'] = EXT_DB_PICS_SRVR + stripname
       piccounter += 1
    else:
       elem1['photo_link'] = "http:" + wikiread_out['pic']     
       if elem1['photo_link'] == "N/A" :
          elem1['photo_link'] = BLANK_IMAGE_URL 
       if matchflag == 1:
          print "Caltour: desc, but no pic ", elem1['name']
    
    # Only retain the entries that have both description and pics
    try:
        if elem1['description'] != "No description available" and elem1['photo_link'] != BLANK_IMAGE_URL:
          if elem1['name'] != higherid:
            # Check if such a name is already present
            presentflag = 0
            for i in Datajson:
              if i['name'] == elem1['name']:
                presentflag = 1
            if presentflag == 0:
                Datajson.append(elem1)
                jsoncount += 1
    except KeyError:
        pass

    print elem1['name']

# Serialize output into json
encoded = json.dumps(Datajson)
f = file('out.json','w')
print >>f, encoded
print "wiki_matches ", Wiki, "ext_db_matches " , ext_db_matches, " ext_db_pics ", piccounter, " counter ", counter, " jsoncount ", jsoncount
