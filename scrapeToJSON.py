from bs4 import BeautifulSoup
import requests
import json
from json.decoder import JSONDecodeError

#####   scrapeToJSON()   #####
#####        INFO        #####
# This program does the main scraping process for getting NFL data from pro-football-reference.com and saves it into "season_XXXX.json" files.
# This program is nominally callable from outside of itself. Users or programs should call it using the name scrapeToJSON(XXXX), where XXXX is
# the year for the data that is being requested. Not all years are expected to work out of the box. No year can be scraped without a 
# "league_XXXX.json" file located inside of the data folder. This file sets up each team's keyName and sets up a variety of other data.

def createNewSeason(target_year):
    try:
        newSeason = json.load(open('data/leagues/'+str(target_year)+'.json'))
        for teamKey in newSeason:
            # initialize stats zeroed-out
            newSeason[teamKey]["stats"] = {
                "games": 0,
                "wins": 0,
                "losses": 0,
                "ties": 0,
                "points": 0,
                "yards": 0,
                "turnovers": 0,
                "opp-points": 0,
                "opp-yards": 0,
                "opp-turnovers": 0
            }
            newSeason[teamKey]["schedule"] = {}
    except:
        print('    ERROR: No League JSON file for year: '+str(target_year))
        print('        !! - TERMINATING PROGRAM EXECUTION - !!')
        exit

    return newSeason

def scrapeToJSON(target_year):
    # set a target file for this season
    season_target_file = 'data/seasons/'+str(target_year)+'.json'
    schedule_target_file = 'data/schedules/'+str(target_year)+'.json'

    try:
        seasonFile = open(season_target_file)
        dot = json.load(seasonFile)
        seasonSchedule = {}
    except JSONDecodeError:
        print("    WARNING: "+season_target_file+" is unexpectedly empty")
        print("        Using empty JSON object instead.")
        dot = createNewSeason(target_year)
    except EnvironmentError:
        print("    WARNING: "+season_target_file+" cannot be found")
        print("        Creating new JSON file")
        dot = createNewSeason(target_year)
    else:
        print("    Scraping NFL data for season: "+str(target_year))

    # load the translate file into a dict
    transFile = open('data/translates/'+str(target_year)+'.json')
    translate = json.load(transFile)
    transFile.close()

    # load the target webpage for scraping
    target_website = "https://www.pro-football-reference.com/years/"+str(target_year)+"/games.htm"
    html_text = requests.get(target_website).text
    soup = BeautifulSoup(html_text, 'html.parser')

    # grab the table from the page for processing
    try:
        table = soup.find('table').find('tbody')
        rows = table.find_all('tr')
    except:
        print('    ERROR: Invalid data returned from URL: '+target_website)
        print('        !! - TERMINATING PROGRAM - !!')
        exit()

    # iterate over each row in the table
    for row in rows:
        columns = row.find_all('td')
        if len(columns) == 0:
            # The week is finished. Continue to next row and proceed.
            continue

        # first, check if the game is concluded...
        gameStatus = "final" if (columns[6].text == "boxscore") else "pregame"

        # store the week number
        weekNumber = row.find('th').text
        if (not(weekNumber.isnumeric())):
            continue

        # next, process all games that still haven't occurred
        if (gameStatus == "pregame"):
            # determine the home and away team keys
            homeTeamKey = translate[columns[5].text.split()[-1].upper()]
            awayTeamKey = translate[columns[3].text.split()[-1].upper()]
            
            #construct and id value for this game 
            id = "week"+weekNumber+"-"+awayTeamKey+"@"+homeTeamKey

            # build two versions of each game to save to both teams' schedules
            homeGame = {
                "opponent"        : awayTeamKey,
                "home-away"       : "Home",
                "day"             : columns[0].text,
                "date"            : columns[1].text,
                "time"            : columns[2].text,
                "status"          : gameStatus,
                "result"          : None,
                "points"          : 0,
                "yards"           : 0,
                "turnovers"       : 0,
                "opp-points"      : 0,
                "opp-yards"       : 0,
                "opp-turnovers"   : 0,
                "id"              : id
            }

            awayGame = {
                "opponent"        : homeTeamKey,
                "home-away"       : "Away",
                "day"             : columns[0].text,
                "date"            : columns[1].text,
                "time"            : columns[2].text,
                "status"          : gameStatus,
                "result"          : None,
                "points"          : 0,
                "yards"           : 0,
                "turnovers"       : 0,
                "opp-points"      : 0,
                "opp-yards"       : 0,
                "opp-turnovers"   : 0,
                "id"              : id
            }

        # third, process all finished games
        else:
            # determine if the game was a tie
            isTie = True if (columns[7].text == columns[8].text) else False

            # build game objects
            if (columns[4].text != "@"):
                # get home/away team keys
                homeTeamKey = translate[columns[3].text.split()[-1].upper()]
                awayTeamKey = translate[columns[5].text.split()[-1].upper()]

                #construct and id value for this game 
                id = "week"+weekNumber+"-"+awayTeamKey+"@"+homeTeamKey

                # determine if the home team won
                isHomeTeamWin = True if (int(columns[7].text) > int(columns[8].text)) else False

                # determine game result for home/away teams
                if (isTie):
                    homeTeamResult = "T"
                    awayTeamResult = "T"
                elif (isHomeTeamWin):
                    homeTeamResult = "W"
                    awayTeamResult = "L"
                else:
                    homeTeamResult = "L"
                    awayTeamResult = "W"

                # build the game object
                homeGame = {
                    "opponent"        : awayTeamKey,
                    "home-away"       : "Home",
                    "day"             : columns[0].text,
                    "date"            : columns[1].text,
                    "time"            : columns[2].text,
                    "status"          : gameStatus,
                    "result"          : homeTeamResult,
                    "points"          : int(columns[7].text),
                    "yards"           : int(columns[9].text),
                    "turnovers"       : int(columns[10].text),
                    "opp-points"      : int(columns[8].text),
                    "opp-yards"       : int(columns[11].text),
                    "opp-turnovers"   : int(columns[12].text),
                    "id"              : id
                }

                awayGame = {
                    "opponent"        : homeTeamKey,
                    "home-away"       : "Away",
                    "day"             : columns[0].text,
                    "date"            : columns[1].text,
                    "time"            : columns[2].text,
                    "status"          : gameStatus,
                    "result"          : awayTeamResult,
                    "points"          : int(columns[8].text),
                    "yards"           : int(columns[11].text),
                    "turnovers"       : int(columns[12].text),
                    "opp-points"      : int(columns[7].text),
                    "opp-yards"       : int(columns[9].text),
                    "opp-turnovers"   : int(columns[10].text),
                    "id"              : id
                }

            else:
                # get home/away team keys
                homeTeamKey = translate[columns[5].text.split()[-1].upper()]
                awayTeamKey = translate[columns[3].text.split()[-1].upper()]

                #construct and id value for this game 
                id = "week"+weekNumber+"-"+awayTeamKey+"@"+homeTeamKey

                # determine if the home team won
                isHomeTeamWin = True if (int(columns[8].text) > int(columns[7].text)) else False

                # determine game result for home/away teams
                if (isTie):
                    homeTeamResult = "T"
                    awayTeamResult = "T"
                elif (isHomeTeamWin):
                    homeTeamResult = "W"
                    awayTeamResult = "L"
                else:
                    homeTeamResult = "L"
                    awayTeamResult = "W"

                # build the game object
                homeGame = {
                    "opponent"        : awayTeamKey,
                    "home-away"       : "Home",
                    "day"             : columns[0].text,
                    "date"            : columns[1].text,
                    "time"            : columns[2].text,
                    "status"          : gameStatus,
                    "result"          : homeTeamResult,
                    "points"          : int(columns[8].text),
                    "yards"           : int(columns[11].text),
                    "turnovers"       : int(columns[12].text),
                    "opp-points"      : int(columns[7].text),
                    "opp-yards"       : int(columns[9].text),
                    "opp-turnovers"   : int(columns[10].text),
                    "id"              : id
                }

                awayGame = {
                    "opponent"        : homeTeamKey,
                    "home-away"       : "Away",
                    "day"             : columns[0].text,
                    "date"            : columns[1].text,
                    "time"            : columns[2].text,
                    "status"          : gameStatus,
                    "result"          : awayTeamResult,
                    "points"          : int(columns[7].text),
                    "yards"           : int(columns[9].text),
                    "turnovers"       : int(columns[10].text),
                    "opp-points"      : int(columns[8].text),
                    "opp-yards"       : int(columns[11].text),
                    "opp-turnovers"   : int(columns[12].text),
                    "id"              : id
                }

        # add this info to each team's dictionary record
        dot[homeTeamKey]["schedule"]["week"+weekNumber] = homeGame
        dot[awayTeamKey]["schedule"]["week"+weekNumber] = awayGame

        # New code for saving to "Schedules" DB
        if not("week"+weekNumber in seasonSchedule.keys()):
            seasonSchedule['week'+weekNumber] = {}
        seasonSchedule['week'+weekNumber][id] = {
                "score"           : '' if homeGame['status'] == 'pregame' else str(homeGame['opp-points'])+"@"+str(homeGame['points']),
                "status"          : homeGame['status']
            }

        
        
    # output new season data back to the season file
    with open(season_target_file, 'w') as seasonFile:
        new_json = json.dumps(dot, indent=4)
        seasonFile.write(new_json)

    seasonFile.close()
    
    # output new schedule data back to the schedule file
    with open(schedule_target_file, 'w') as scheduleFile:
        new_json = json.dumps(seasonSchedule, indent=4)
        scheduleFile.write(new_json)

    scheduleFile.close()
