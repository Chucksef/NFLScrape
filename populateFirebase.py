import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os

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


    # Save the schedule data to the Schedules node
    # First, open the target schedule
    with open("data/schedules/"+str(target_year)+".json", "r") as schedule:
        schedule_data = json.load(schedule)

    # Second, set the reference for the schedule node
    scheduleRef = db.reference("/schedules/"+str(target_year))

    # Third, save the data to the DB
    print("    Populating Firebase for schedule: "+str(target_year))
    scheduleRef.set(schedule_data)

