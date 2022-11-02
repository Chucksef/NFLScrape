from scrapeToJSON import scrapeToJSON
from processStats import processStats
from populateFirebase import populateFirebase
from populateFirebase import updateSchedule
from populateFirebase import updateWeek
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
    updateSchedule(args.season)
else:
    # otherwise, just process like normal for the current year
    today = date.today()
    day = today.day
    now = str(datetime.now()).split('.')[0] # chop off fractions of seconds
    hour = now.split(' ')[1].split(':')[0]
    month = today.month
    year = today.year

    # output to console for logging
    print(now + " ---- Running NFLScrape")

    # if it is not yet May, revert to previous year
    if (month < 9): year -= 1

    scrapeToJSON(year)
    processStats(year)
    populateFirebase(year)
    updateSchedule(year)
    updateWeek(year, day, hour)