from scrapeToJSON import scrapeToJSON
from processStats import processStats
from populateFirebase import populateFirebase

# This utility rebuilds all seasons and re-uploads them to the server

# MAIN CODE EXECUTION BELOW:
seasons = [2022,2021,2020,2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002]

for season in seasons:
    print("Rebuilding season.json file for season: "+str(season))
    scrapeToJSON(season)
    processStats(season)
    populateFirebase(season)
