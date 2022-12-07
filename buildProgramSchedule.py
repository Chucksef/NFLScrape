from populateFirebase import updateWeek
from utilities.getTodayInfo import getTodayInfo
import json
from populateFirebase import populateFirebase
from processStats import processStats
from scrapeToJSON import scrapeToJSON
from scrapeLiveScores import scrapeLiveScores
from setPickable import setPickable

# Weekly Schedule:
# Tuesday @ 3:30am buildProgramSchedule will be run as the last scheduled event from the previous week
# It will run and programSchedule.txt will be filled out with schedule information for the coming week

### Program Execution:
def buildProgramSchedule(dateInfo):
    #   immediately call scrapeToJSON to ensure up-to-date schedule information for the coming week
    scrapeToJSON(dateInfo)
    processStats(dateInfo)
    populateFirebase(dateInfo)

    #   directly call updateWeek() to enable picking for the next week's games.
    updateWeek(dateInfo)
    setPickable(True)

    #   Then scrape live scores to capture any odds information for the upcoming week
    scrapeLiveScores(dateInfo)

    #   create a variable to hold the new schedule
    newSchedule = []

    #   open the JSON schedule and get the start times of all games
    schedule_target_file = 'data/schedules/'+str(dateInfo['season'])+'.json'
    seasonFile = open(schedule_target_file)
    schedJSON = json.load(seasonFile)
    currWeek = schedJSON['status']['currentWeek'].split("-")[1]
    gameStartTimes = [int(schedJSON[currWeek][matchup]['date']+schedJSON[currWeek][matchup]['time']+'00') for matchup in schedJSON[currWeek]]
    gameStartTimes = list(dict.fromkeys(gameStartTimes))        # De-dupe list
    gameStartTimes.sort()                                       # Sort the list
    gameEndTimes = [time+43000 for time in gameStartTimes]      # Derive a list of end times

    #   Merge the time-windows if they overlap
    gameTimeWindows = []
    for idx, sTime in enumerate(gameStartTimes):
        eTime = gameEndTimes[idx]
        if idx == 0:
            gameTimeWindows.append([sTime, eTime])
        else:
            if sTime < gameTimeWindows[-1][1]:
                gameTimeWindows[-1][1] = eTime
            else: 
                gameTimeWindows.append([sTime, eTime])
    


    #   Beginning now, schedule scrapeLiveScores() every 2 hours until the first game's kickoff
    runTime = int(dateInfo['timestr'])
    schedTime = gameTimeWindows[0][0] - 500                    # make last update 5 minutes prior to kickoff
    # correct for base-60 subtraction issues
    pref = str(schedTime)[0:10]
    mins = str(schedTime)[10:-2]
    secs = str(schedTime)[-2:]
    if int(mins) > 59:
        mins = str(int(mins) - 40).zfill(2)
        schedTime = int(pref+mins+secs)
    # actually run the loop and fill out the schedule
    while schedTime >= runTime:
        newSchedule.insert(0, str(schedTime)+'---makeVegasPicks')
        newSchedule.insert(0, str(schedTime)+'---scrapeLiveScores')
        schedTime = schedTime-20000
        # Correct for base-60 weirdness
        year = str(schedTime)[0:4]
        mnth = str(schedTime)[4:6]
        days = str(schedTime)[6:8]
        hour = str(schedTime)[8:10]
        mins = str(schedTime)[10:12]
        secs = str(schedTime)[12:]
        # check for various rollover scenarios
        if int(hour) > 24:
            hour = str(int(hour) - 76).zfill(2)
        if int(days) < 1:
            maxDays = 31
            if int(mnth)-1 in [9,11]: maxDays = 30
            days = str(maxDays).zfill(2)
            mnth = str(int(mnth) - 1).zfill(2)
        if int(mnth) < 1:
            mnth = "12"
            year = str(int(year) - 1)
        schedTime = int(year+mnth+days+hour+mins+secs)


    #   Schedule setPickable() to be called exactly when the first game starts to disallow picking after the games start
    newSchedule.append(str(gameTimeWindows[0][0])+"---setPickable False")

    #   Set a var to hold the scrape time
    finalScrape = None

    #   Loop over each game-window
    for window in gameTimeWindows:
        currTime = window[0]
        endTime = window[1]
        while currTime < window[1]:
            # Schedule scrapeLiveScores() every 15 seconds within each window
            newSchedule.append(str(currTime)+"---scrapeLiveScores")
            currTime += 15
            # correct for base-60 weirdness
            pref = str(currTime)[0:8]
            hour = str(currTime)[8:-4]
            mins = str(currTime)[10:-2]
            secs = str(currTime)[-2:]
            if int(secs) > 59:
                secs = str(int(secs) - 60).zfill(2)
                mins = str(int(mins) + 1).zfill(2)
                if int(mins) > 59:
                    mins = str(int(mins) - 60).zfill(2)
                    hour = str(int(hour) + 1).zfill(2)
            currTime = int(pref+hour+mins+secs)
        # Schedule scrapeToJSON() 8 hours after the window closes
        scrapeTime = endTime+80000
        year = str(scrapeTime)[0:4]
        mnth = str(scrapeTime)[4:6]
        days = str(scrapeTime)[6:8]
        hour = str(scrapeTime)[8:10]
        mins = str(scrapeTime)[10:12]
        secs = str(scrapeTime)[12:]
        # check for various rollover scenarios
        if int(hour) > 24:
            hour = str(int(hour) - 24).zfill(2)
            days = str(int(days) + 1).zfill(2)
            maxDays = 31
            if int(mnth) in [9,11]: maxDays = 30
            if int(days) > maxDays:
                days = "01"
                mnth = str(int(mnth) + 1).zfill(2)
                if int(mnth) > 12:
                    mnth = "01"
                    year = str(int(year) + 1)
        scrapeTime = year+mnth+days+hour+mins+secs
        finalScrape = scrapeTime
        newSchedule.append(str(scrapeTime)+"---scrapeToJSON")
        newSchedule.append(str(scrapeTime)+"---processStats")
        newSchedule.append(str(scrapeTime)+"---populateFirebase")

    # check if it is the final week
    if int(dateInfo['weekID'].split('-')[1].replace('week','')) != 18:
        # add a line to schedule this program to run again in a week
        newSchedule.append(str(finalScrape)+"---buildProgramSchedule")

    with open('programSchedule.txt', 'w') as f:
        for line in newSchedule:
            f.write(f"{line}\n")

# di = getTodayInfo()
# buildProgramSchedule(di)