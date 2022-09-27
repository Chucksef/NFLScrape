import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('C:/Users/Charles Crouse/Documents/firebaseAdmin/nflscrape-firebase-adminsdk-dqvc3-49b861c0cc.json')
app = firebase_admin.initialize_app(cred, {
        'databaseURL':'https://nflscrape-default-rtdb.firebaseio.com/'
    })

def populateFirebase(target_year):
    # First, open the target season
    with open("data/seasons/"+str(target_year)+".json", "r") as season:
        season_data = json.load(season)

    ref = db.reference("/seasons/"+str(target_year))

    print("Populating Firebase for season: "+str(target_year))
    ref.set(season_data)