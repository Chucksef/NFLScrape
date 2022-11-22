from scrapeToJSON import scrapeToJSON
from processStats import processStats
from populateFirebase import populateFirebase
from populateFirebase import updateSchedule
from populateFirebase import updateWeek
from populateFirebase import updateScores
from utilities import getTodayInfo
from scrapeLiveScores import scrapeLiveScores
from utilities import getProgramScheduleCommand
import time

# Program Description:
# This program is designed to run every minute on a schedule.
#
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
# 1) get all date/time info to feed into the scheduler
dateInfo = getTodayInfo.getTodayInfo()
currTime = dateInfo['epochSecs']
endTime = currTime + 45

iter = 0
print("Running until "+str(endTime))

# 2) begin processing loop
while currTime < endTime:
    # update loop variables
    remTime = endTime - currTime
    iter += 1
    # 3) read the programSchedule
    command = getProgramScheduleCommand.getProgramScheduleCommand(dateInfo['timestr'])
    print("    Running Command "+str(iter)+": '"+command+"' with "+str(remTime)+" remaining in loop.")
    # 4) execute the returned command
    if command == "scrapeToJSON":
        scrapeToJSON(dateInfo)
    if command == "scrapeLiveScores":
        scrapeLiveScores(dateInfo)
    elif command == "processStats":
        processStats(dateInfo)
    elif command == "populateFirebase":
        populateFirebase(dateInfo)
    elif command == "updateWeek":
        updateWeek(dateInfo)
    elif command == "updateScores":
        updateScores(dateInfo)
    elif command == "updateSchedule":
        updateSchedule(dateInfo['season'])
    else:
        print("  Finished Command "+str(iter)+": "+command)
    
    time.sleep(10)
    currTime = int(time.time())

print('End of timed program execution')

