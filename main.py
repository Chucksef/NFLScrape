from scrapeToJSON import scrapeToJSON
from processStats import processStats
from populateFirebase import populateFirebase
from datetime import date

# Goals:
# This is where my current to-do list will go...

# MAIN CODE EXECUTION BELOW:
today = date.today()
month = today.month
year = today.year

# if it is not yet May, revert to previous year
if (month < 5): year -= 1

scrapeToJSON(year)
processStats(year)
populateFirebase(year)