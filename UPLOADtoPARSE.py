#! /usr/bin/env python

# Guided Area
# Python script that uploads the given sys.arg[1] json file to parse.com
# last edited: Nov 30, 2012

import os
import json
import sys

print "Starting Uploader"

# Parse.com authorization keys
APPLICATION_ID="bAMGYsME9tgqpa4uIeeT49FgsgMrUbl8pKbirrmK#mnbv"
REST_API_KEY="7W88qLyGJtfEIlGcKo2vaOvfXhGwDHWaJFT7IcNz#mnbv"

# Try to access the file containing json information
try:
	 File_to_Post=sys.argv[1]
except:
	 print "MAKE SURE YOU PASS \"File_to_Post\" AS AN ARGUMENT"
	 sys.exit(0)

# Name of the parse.com database it's content is written to 
Database="TEST" # put actual name here

# Check if the json file is passed
if File_to_Post == "":
	print "MAKE SURE YOU PASS \"File_to_Post\" AS AN ARGUMENT"
	sys.exit (0)

# Parse the JSON content
fileh = open(File_to_Post)
objs = json.load(fileh)

# Iterate through the lines in the list
for o in objs:

    o = json.dumps(o)
    # debug print
    print o

    # make an http post request to parse.com and execute it
    command1 = 'curl -X POST \
     -H "X-Parse-Application-Id: %s" \
     -H "X-Parse-REST-API-Key: %s"    \
     -H "Content-Type: application/json"          \
     -d \'%s\' \
      https://api.parse.com/1/classes/\'%s\'' % (APPLICATION_ID, REST_API_KEY, o, Database)
    os.system(command1)

fileh.close()
