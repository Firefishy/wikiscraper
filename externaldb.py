# wikiscraper
# author: Timur Bazhirov
# last updated Nov 30, 2012 
# 
# This function searches if a particular named article is present in an
# external database file, if yes - grabs the first description 
# (and a photo url)

import os
import sys
import json
import types
import re

def Caltour(external_xml_database):

    filename = file(external_xml_database,'r')
    Data1 = []

    for line in filename:
      if '<item>' in line:
        Name = filename.next().rstrip('\\')
        Name = Name[:-3]
        Type = filename.next().rstrip('\\')
        Built = filename.next().rstrip('\\')
        Built = Built[:-3]
        Type1 = filename.next().rstrip('\\')
        Type = Type[:-3]
        Type1 = Type1[:-3]
        Description = filename.next().rstrip('\\')
        Description = Description[:-3]
        Coord = filename.next().rstrip('\\')
        Data1.append([ ["name", Name], ["description", Description], ["built", Built]])
    
    return Data1