import json
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from utilities import getTodayInfo

thisPath = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
cred = credentials.Certificate(thisPath+'/credentials/nflscrape-firebase-adminsdk-dqvc3-ae425d7a17.json')
app = firebase_admin.initialize_app(cred, {
        'databaseURL':'https://nflscrape-default-rtdb.firebaseio.com/'
    })

def updateFirebase(ref, updateData):
    updateRef = db.reference(ref)
    updateRef.update(updateData)

def populateFirebase(dateInfo):
    target_year = dateInfo['season']
    # Save the season data to the Seasons node
    # First, open the target season
    with open("data/seasons/"+str(target_year)+".json", "r") as season:
        season_data = json.load(season)

    # Second, set the reference for the season
    seasonRef = db.reference("/seasons/"+str(target_year))

    # Third, save the data to the DB
    print("    Populating Firebase for season: "+str(target_year))
    seasonRef.set(season_data)


def updateSchedule(target_year):
    # Using the same program flow as above, save the schedule data to the Schedules node
    with open("data/schedules/"+str(target_year)+".json", "r") as schedule:
        schedule_data = json.load(schedule)
    scheduleRef = db.reference("/schedules/"+str(target_year))
    print("    Populating Firebase for schedule: "+str(target_year))
    scheduleRef.set(schedule_data)


def updateWeek(dateInfo):
    # Update the current week and set whether it is editable or not in the Schedules node
    year = dateInfo['season']
    day = dateInfo['day']
    hour = dateInfo['hour']
    currentWeek = ''
    weekEnabled = True
    # First, open the relevant schedule json file
    with open("data/schedules/"+str(year)+".json", "r") as schedule:
        schedule_data = json.load(schedule)
    # Second, determine the earliest week with "pregame" games in it
    currWeekMatchups = None
    for week in schedule_data:
        if week == 'status': continue
        if currentWeek != '':
            # Create a list of all the week's matchups
            currWeekMatchups = schedule_data[week]
            break
        for matchup in schedule_data[week]:
            matchData = schedule_data[week][matchup]
            if matchData['status'] == 'pregame':
                currentWeek = str(year)+"-"+week
                dateInfo['weekID'] = str(year)+"-"+week
                break
            
    # Third, determine the start time (MDT) of the first game
    earliestGame = 99999999999999
    for matchup in currWeekMatchups:
        matchTime = currWeekMatchups[matchup]['date']+currWeekMatchups[matchup]['time']+'00'
        if int(matchTime) < int(earliestGame): earliestGame = matchTime
    
    # Fourth, disable picking this week if it is past the first scheduled game for the given week
    if (int(day) == 3 and int(hour) >= 19) or (int(day) > 3) or (int(day) == 0):
        print("day: "+str(day))
        weekEnabled = False
    # Fifth, write these two things out to the "Schedules" root node
    scheduleRef = db.reference("/schedules/status/")
    currentWeekData = {
        "currentPickable": weekEnabled,
        "currentWeek"    : currentWeek
    }
    print("    Updating Firebase CurrentWeek to "+currentWeek+" and setting pickability to: "+str(weekEnabled))
    scheduleRef.update(currentWeekData)
    schedule_data['status'] = currentWeekData

    # output new schedule data back to the schedule file
    with open("data/schedules/"+str(year)+".json", "w") as scheduleFile:
        new_json = json.dumps(schedule_data, indent=4)
        scheduleFile.write(new_json)

    scheduleFile.close()


def checkPrediction(year, weekID, matchupID, prediction):
    predictedWinner = prediction.split("@")[0]
    predictionValue = prediction.split("@")[1]
    # load the schedule DB from file
    with open("data/schedules/"+year+".json", "r") as schedule:
        scheduleData = json.load(schedule)
        matchup = scheduleData[weekID][matchupID]
        awayScore = int(matchup['score'].split('@')[0])
        homeScore = int(matchup['score'].split('@')[1])
        windex = 0 if awayScore > homeScore else 1
        winner = matchupID.split('-')[1].split("@")[windex] if homeScore != awayScore else 'TIE'
        if predictedWinner == winner:
            return int(predictionValue)
        else:
            return 0

    

### FUNCTION FOR UPDATING ALL WEEKLY SCORE DATA IN USER PROFILES & IN LEAGUES
def updateScores(dateInfo):
    year = dateInfo['season']
    weekID = dateInfo['weekID']
    # Get all user data from DB
    userRef = db.reference('/accounts/users/')
    allUsers = userRef.get()
    year = str(year)
    weekID = str(weekID)

    print("    Updating Firebase User Scores for weekID: "+weekID)

    # Iterate through each user
    for userKey in allUsers:
        userData = allUsers[userKey]
        # Check if they have picks for current week
        if 'picks' in userData:
            if year in userData['picks']:
                if weekID in userData['picks'][year]:
                    # If so, get the Current Week's picks
                    weekScore = 0
                    weekPicks = userData['picks'][year][weekID]
                    for key in weekPicks:
                        if key == 'score':
                            continue
                        else:
                            prediction = weekPicks[key]
                            earnedPoints = checkPrediction(year, weekID, key, prediction)
                            weekScore += earnedPoints
                            week = weekID.split("-")[1]
                    # Update the database with the score information for this user
                    updateRef = db.reference('/accounts/users/'+userKey+'/picks/'+str(year)+'/'+week)
                    updateRef.update({'score':str(weekScore)})



### FUNCTION FOR UPDATING ALL LEAGUE SCORES IN LEAGUES DATABASE
### NO LONGER NEEDED. LOGIC MOVED TO FRONT-END ON LEAGUE VIEW ###
def updateLeagues(year, weekID):
    # Get all league data from DB
    leaguesRef = db.reference('/leagues/')
    allLeagues = leaguesRef.get()
    week = weekID.split("-")[1]
    year = str(year)

    print("    Updating Firebase League Scores for season: "+str(year))

    # Iterate over each league
    for leagueKey in allLeagues:
        leagueData = allLeagues[leagueKey]

        # skip this league if the year or week are out of bounds
        if int(leagueData['season']) != int(year): 
            continue
        if int(leagueData['startWeek'].replace('week','')) > int(week.replace('week','')): 
            continue
        else:
            leagueStartWeekNum = int(leagueData['startWeek'].replace('week',''))

        # Get the league's list of users and iterate over them
        leagueUsers = leagueData['users']
        for userKey in leagueUsers:
            tempLeagueUser = leagueUsers[userKey]
            # query the DB for this user's score @ this year & week
            # queryRef = db.reference('/accounts/users/'+userKey+'/picks/'+str(year)+'/'+week+'/score')
            queryRef = db.reference('/accounts/users/'+userKey)
            results = queryRef.get()
            try:
                tempLeagueUser[week] = results['picks'][year][week]['score']
            except:
                tempLeagueUser[week] = '0'

            # calculate the total score for this user in this League
            userTotal = 0
            for key in tempLeagueUser:
                if key == "total" or key == "name": continue
                weekNum = int(key.replace('week',''))
                if int(weekNum) < int(leagueStartWeekNum): continue
                weekScore = int(tempLeagueUser[key])
                userTotal += weekScore
            

            # Update the league database with the score information for this user
            updateRef = db.reference('/leagues/'+leagueKey+'/users/'+userKey)
            updateRef.update({week:tempLeagueUser[week],'total':userTotal,'name':results['email']})