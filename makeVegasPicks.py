import json
from populateFirebase import updateFirebase
from utilities.getTodayInfo import getTodayInfo

def makeVegasPicks(dateInfo):
    season = dateInfo['season']

    # open the schedule for comparison
    schedule_target_file = 'data/schedules/'+str(season)+'.json'
    seasonFile = open(schedule_target_file)
    schedJSON = json.load(seasonFile)

    # get current week from schedule
    currWeek = schedJSON['status']['currentWeek'].split("-")[1]
    currWeekNum = int(currWeek.replace("week",''))

    # loop through each matchup to ensure odds exist for each
    matchups = schedJSON[currWeek]

    allOdds = []
    weekHasAllOdds = True
    for matchup in matchups:
        curMatch = matchups[matchup]
        if 'odds' in curMatch: 
            matchObj = {
                'matchID': matchup,
                'home': matchup.split("-")[1].split("@")[1],
                'away': matchup.split("-")[1].split("@")[0],
                'pick': curMatch['odds'].split(" ")[0],
                'val': float(curMatch['odds'].split(" ")[1])
            }
            if matchObj['home'] == matchObj['pick']:
                matchObj['val'] -= .1
            allOdds.append(matchObj)
        else:
            weekHasAllOdds = False

    if weekHasAllOdds:
        print("    Making Picks for Vegas@Picks")
        # sort by value
        sortedMatchups = sorted(allOdds, key=lambda d: d['val'])
        # Loop over sortedMatchups and update the DB at '/accounts/users/0vDOxwAHJEPcx6ZqZsvL5Jh4n2c2/picks/str(season)/currWeek'
        for idx, matchup in enumerate(sortedMatchups):
            pickVal = str(len(sortedMatchups) - idx)
            pickName = matchup['pick']
            if pickName == 'WSH': 
                pickName = 'WAS'
            ref = '/accounts/users/0vDOxwAHJEPcx6ZqZsvL5Jh4n2c2/picks/'+str(season)+'/'+currWeek
            updateVal = matchup['matchID']
            update = {
                updateVal: pickName+"@"+pickVal
            }
            updateFirebase(ref, update)
        pass
    else:
        print("    Cannot generate Vegas Picks; Week does not Have All Odds")

# di = getTodayInfo()
# makeVegasPicks(di)
    