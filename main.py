from scrapeToJSON import scrapeToJSON
from processStats import processStats
from populateFirebase import populateFirebase
from datetime import date, datetime

# Goals:
# This is where my current to-do list will go...
# 1) COMPLETED -- Re-do logging (print()) system-wide

# MAIN CODE EXECUTION BELOW:
today = date.today()
now = str(datetime.now()).split('.')[0] # chop off fractions of seconds
month = today.month
year = today.year

# output to console for logging
print(now + " ---- Running NFLScrape")

# if it is not yet May, revert to previous year
if (month < 5): year -= 1

scrapeToJSON(year)
processStats(year)
populateFirebase(year)