from scrapeToJSON import scrapeToJSON
from processStats import processStats
from populateFirebase import populateFirebase
from datetime import date, datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--season', type=int)
args = parser.parse_args()

# Goals:
# This is where my current to-do list will go...
# 1) COMPLETED -- Re-do logging (print()) system-wide

# MAIN CODE EXECUTION BELOW:
if (args.season):
    # run the three programs for just this year
    scrapeToJSON(args.season)
    processStats(args.season)
    populateFirebase(args.season)
else:
    # otherwise, just process like normal for the current year
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
    updateSchedules(year)