from scrapeToJSON import scrapeToJSON
from processStats import processStats
from populateFirebase import populateFirebase

# Goals:
# 1) COMPLETED -- Move data into type-separated folders
# 2) COMPLETED -- Create year-specific translate files
# 3) COMPLETED -- Move firebase credentials into data folder
# 4) COMPLETED -- Add firebase info to .gitignore

years = [2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]

# MAIN CODE EXECUTION BELOW:

for year in years:
    scrapeToJSON(year)
    processStats(year)
    populateFirebase(year)