# wikiscraper
# Wikipedia scraper based upon openstreetmaps xml data
# Guided Area package
# ver. 30 Nov 2012

===========

Way to use:

1. Go to openstreetmaps.com to generate osm data file in xml format with all map information in a relatively small (city downtown, university campus etc) area (example xml output is given for UC Berkeley campus)

2. Use scraper.py to create json array with buildings perimeter border geopoints and wikipedia-based description
2a. Right now "places.xml" file is used as a backup database for scraper as it has much info about for UCB campus

3. Use UPLOADtoPARSE to upload the content into parse.com