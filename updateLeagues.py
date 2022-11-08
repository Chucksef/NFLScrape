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




### MAIN
# Get the current season and week from the DB
statusRef = db.reference('/schedules/status/')
statusData = statusRef.get()
currentWeek = statusData['currentWeek']
currentYear = currentWeek.split('-')[0]
currentWeek = 'week9'
currentPickable = statusData['currentPickable']
updateLeagues(currentYear, currentWeek)