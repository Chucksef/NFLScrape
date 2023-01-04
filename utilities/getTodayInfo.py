from datetime import date, datetime
import time
import json

def getTodayInfo():
    today = date.today()
    day = datetime.now().weekday()
    now = str(datetime.now()).split('.')[0] # chop off fractions of seconds
    hour = now.split(' ')[1].split(':')[0]
    mins = str(now.split(' ')[1].split(':')[1])
    secs = str(now.split(' ')[1].split(':')[2])
    month = today.month
    currYear = today.year

    timestr = str(currYear)+str(month).zfill(2)+datetime.now().strftime("%d").zfill(2)+str(hour).zfill(2)+mins.zfill(2)+secs.zfill(2)

    # if it is not yet May, revert to previous year
    season = (currYear - 1) if (month < 9) else currYear

    # get the current week from the current JSON schedule
    with open("data/schedules/"+str(season)+".json", "r") as schedule:
        schedule_data = json.load(schedule)
    
    weekID = schedule_data['status']['currentWeek']

    # get the number of seconds in this epoch
    epochSecs = int(time.time())

    return {
        'today': today,
        'day': day,
        'now': now,
        'hour': hour,
        'month': month,
        'season': season,
        'year': currYear,
        'weekID': weekID,
        'epochSecs': epochSecs,
        'timestr': timestr
    }