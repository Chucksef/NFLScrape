import json
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

thisPath = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
cred = credentials.Certificate(thisPath+'/credentials/nflscrape-firebase-adminsdk-dqvc3-ae425d7a17.json')
app = firebase_admin.initialize_app(cred, {
        'databaseURL':'https://nflscrape-default-rtdb.firebaseio.com/'
    })

def populateFirebase(target_year):
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


def updateWeek(year, day, hour):
    # Update the current week and set whether it is editable or not in the Schedules node
    # First, open the relevant schedule json file
    currentWeek = ''
    weekEnabled = True
    with open("data/schedules/"+str(year)+".json", "r") as schedule:
        schedule_data = json.load(schedule)
    # Second, determine the earliest week with "pregame" games in it
    for week in schedule_data:
        if any([True for k,v in schedule_data[week].items() if v == {'score':'','status':'pregame'}]):
            currentWeek = str(year)+"-"+week
            break
    # Third, disable picking this week if it is past 6:30PM on Thursday
    if (day > 2 and hour >= 19):
        weekEnabled = False
    # Fourth, write these two things out to the "Schedules" root node
    scheduleRef = db.reference("/schedules/status/")
    currentWeekData = {
        "currentPickable": weekEnabled,
        "currentWeek"    : currentWeek
    }
    print("    Updating Firebase CurrentWeek to "+currentWeek+" and setting pickability to: "+str(weekEnabled))
    scheduleRef.update(currentWeekData)