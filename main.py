from scrapeToJSON import scrapeToJSON
from processStats import processStats
from populateFirebase import populateFirebase
from populateFirebase import updateSchedule
from populateFirebase import updateWeek
from populateFirebase import updateLeagues
from populateFirebase import updateScores
from datetime import date, datetime
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--season', type=int)
args = parser.parse_args()

# Program Description:
# The NFLScrape package maintains and updates the NFLScrape database on Google Firebase, which
# hosts all of the data needed to run the Gridiron Pickem' webapp. This program is usually
# going to be run on a schedule, which is governed by Crontab. When run this way, it will be
# called with no parameters, and the program will look at the current date & time of day to 
# determine what operations need to be run. Alternatively, this program can also be run 
# manually by calling python main.py --season XXXX from the CLI. This will prompt the program
# to create data for and/or update the specified season.
#
# Generally speaking, this package should make keeping up-to-date NFL data very simple in-
# season. Between seasons, there is the very real chance that work will need to be done to
# adjust for websites changing the way they format season or game data. Ideally, all of this
# work will be performed during pre-season, when stats websites are up but picks are not yet
# being made. As a fallback, the author recommends keeping the logic for scraping off of 
# pro-football-reference.com. While this data is not 'live' in any sense, its formatting is
# the most consistent and predictable, so should break very rarely.

# MAIN CODE EXECUTION BELOW:
if (args.season):
    # run the three programs for just this year
    scrapeToJSON(args.season)
    processStats(args.season)
    populateFirebase(args.season)
    updateSchedule(args.season)
else:
    # First, get all date/time info to feed into the scheduler
    today = date.today()
    day = datetime.now().weekday()
    now = str(datetime.now()).split('.')[0] # chop off fractions of seconds
    hour = now.split(' ')[1].split(':')[0]
    month = today.month
    year = today.year

    # Second, send this data to the scheduler, which will return a list of tasks

    # Third, iterate over this list of tasks and log the results of each operation

    # output to console for logging
    print(now + " ---- Running NFLScrape")

    # if it is not yet May, revert to previous year
    if (month < 9): year -= 1

    # get the current week from the current JSON schedule
    with open("data/schedules/"+str(year)+".json", "r") as schedule:
        schedule_data = json.load(schedule)
    
    weekID = schedule_data['status']['currentWeek']

    scrapeToJSON(year)
    processStats(year)
    populateFirebase(year)
    updateSchedule(year)
    updateWeek(year, day, hour)
    updateScores(year, weekID)
    updateLeagues(year, weekID)