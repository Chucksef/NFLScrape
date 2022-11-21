from datetime import date, datetime
import json

def getTodayInfo():
    today = date.today()
    day = datetime.now().weekday()
    now = str(datetime.now()).split('.')[0] # chop off fractions of seconds
    hour = now.split(' ')[1].split(':')[0]
    month = today.month
    currYear = today.year

    # Second, send this data to the scheduler, which will return a list of tasks

    # Third, iterate over this list of tasks and log the results of each operation

    # output to console for logging
    print(now + " ---- Running NFLScrape")

    # if it is not yet May, revert to previous year
    season = (currYear - 1) if (month < 9) else currYear

    # get the current week from the current JSON schedule
    with open("data/schedules/"+str(currYear)+".json", "r") as schedule:
        schedule_data = json.load(schedule)
    
    weekID = schedule_data['status']['currentWeek']

    return {
        'today': today,
        'day': day,
        'now': now,
        'hour': hour,
        'month': month,
        'season': season,
        'year': currYear,
        'weekID': weekID
    }