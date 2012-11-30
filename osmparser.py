# wikiscraper
# author: Timur Bazhirov - bazhirov.com
# last edited: Nov 30, 2012
#
# This function parses the given XML file to grab the buildings 
# and the coordinates of their border points.
# Output is a python array.
# For more explanation of the data format and imposm.parser
# callbacks see http://dev.omniscale.net/imposm.parser/

import os
import sys
import json
import types
from imposm.parser import OSMParser
import re

# initiate necessary variables
higherid = "University of California, Berkeley"

# array where the imposm data is being stored
Data = []


''' fn used to check if a string contains certain substring'''

def check_if_plaza(string):
  
  if "Gate" in string or "Glade" in string or "Plaza" in string:
     return True
  else:
     return False


''' fn used to associate gps coordinates with the known OSM ID'''

def coords_callback(coords):  
  # scanning all coords in file  
  for osm_id, lon, lat in coords: 
    count = -1 # counter to count elements in Data
    # scanning Data

    for osmid, refs, nm, higherid in Data:  
       count += 1
       # scanning OSM_IDs of border points
       count1 = -1
       for id_ in refs[1]:  
         count1 += 1
         if id_==osm_id:
            # adding lon and lat to Data
            Data[count][1][1][count1] = [["lat", lat], ["lon",lon]]



'''class used to get the OSMIDs of borders'''

class WaysOsmIdExtractor(object):
    
    def border(self, ways):
        #callback method for buildings
        for osmid, tags, refs in ways:
            if 'name' in tags:
                Data.append([ ["thisid", osmid], ["points", refs], ["name",tags['name']], ["higherid", higherid]])
    
    def points(self, nodes):
        for osmid, tags, coord in nodes:

                if 'name' in tags:
                  if check_if_plaza(tags['name']):
                    Data.append([ ["thisid", osmid], ["points", [[["lat", coord[1]], ["lon",coord[0]]]]], ["name",tags['name']], ["higherid", higherid]])
                    print  Data[len(Data) - 1]


        
'''fn that instantiates counter and parser and starts parsing'''

def Parse(xml_file_name,_higherid):

    # id of a higher element in the map hierarchy of Guided Area 
    # (id of the area that contains the current elements)
    higherid = _higherid

    buildings = WaysOsmIdExtractor()
    p = OSMParser(concurrency=4, ways_callback=buildings.border, nodes_callback=buildings.points)
    p.parse_xml_file(xml_file_name)

    b = OSMParser(concurrency=4, coords_callback=coords_callback)
    b.parse_xml_file(xml_file_name)

    return Data


# KNOWN BUGS:
    # 
    # These points don't show up in callback for some reason
    # Was on line 44 above:
    # if osm_id == 286632968 or osm_id ==  365795484 or osm_id == 286633014: 
    #  print "EVRIKA!!!"
