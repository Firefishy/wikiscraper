# wikiscraper

===========

Wikipedia scraper based upon OpenStreetMap xml data

Guided Area package

===========

Way to use:

1. Go to openstreetmap.org to generate osm data file in xml format with all map information in a relatively small (city downtown, university campus etc) area (example xml output is given for UC Berkeley campus)

2. Use scraper.py to create json array with buildings perimeter border geopoints and wikipedia-based description
2a. Right now "places.xml" file is used as a backup database for scraper as it has much info about for UCB campus

3. Use UPLOADtoPARSE to upload the content into parse.com


===================================================================

Files\folders decription:

The main executable wrapper 

-rwxr-xr-x  scraper.py 

The function that posts an httprequest to wikipedia (actual scraper) 

-rw-r--r--  wikiread.py

Openstreetmap xml file parser 

-rw-r--r--  osmparser.py

Optionary additional source of information - external database handling script (complimentary to wikipedia) 

-rw-r--r--  externaldb.py

GPS coordinates conversion tool 

-rw-r--r--  conversion.py

Directories with input and output files 

drwxr-xr-x  json_example_output 

drwxr-xr-x  openstreetmap_example_data 

Upload to Parse.com script 

-rwxr-xr-x  UPLOADtoPARSE.py

External database 

-rw-r--r--  ./external_database/places.xml

Readme 

-rw-r--r--  README.md
