from populateFirebase import updateFirebase
from utilities.getTodayInfo import getTodayInfo
from utilities.updateData import updateData

def setPickable(pickable):
    dateInfo = getTodayInfo()
    season = dateInfo['season']
    
    # Update data on the local JSON file
    firebase_ref = '/schedules/status/'
    firebase_update = {
        'currentPickable': pickable,
    }
    updateFirebase(firebase_ref, firebase_update)

    # Update pickable on firebase
    updateData('schedules/'+str(season)+'.json', 'status/currentPickable', pickable)

# setPickable(False)
    