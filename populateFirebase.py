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
    # First, open the target season
    with open("data/seasons/"+str(target_year)+".json", "r") as season:
        season_data = json.load(season)

    ref = db.reference("/seasons/"+str(target_year))

    print("    Populating Firebase for season: "+str(target_year))
    ref.set(season_data)