from scrapeToJSON import scrapeToJSON
from processStats import processStats
from populateFirebase import populateFirebase

# Goals:
# 1) COMPLETED -- Move data into type-separated folders
# 2) COMPLETED -- Create year-specific translate files
# 3) Move firebase credentials into data folder
# 4) Add firebase info to .gitignore

# MAIN CODE EXECUTION BELOW:
scrapeToJSON(2016)
scrapeToJSON(2017)
scrapeToJSON(2018)
scrapeToJSON(2019)

processStats(2016)
processStats(2017)
processStats(2018)
processStats(2019)

populateFirebase(2016)
populateFirebase(2017)
populateFirebase(2018)
populateFirebase(2019)