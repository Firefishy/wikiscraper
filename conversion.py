# -*- coding: utf-8 -*-
# wikiscraper
# Function that converts GPS coordinates in degrees into decimals #
# Last updated: Nov 30, 2012

def conversion(old):

    direction = {'N':-1, 'S':1, 'E': -1, 'W':1}
    new = old.replace('°',' ').replace('′',' ').replace('″',' ')

    new = new.split()
    new_dir = new.pop()
    new.extend([0,0,0])

    return (float(new[0])+float(new[1])/60.0+float(new[2])/3600.0) * direction[new_dir]