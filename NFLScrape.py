from bs4 import BeautifulSoup
import requests
import json
from json.decoder import JSONDecodeError

# GOALS: 
#   1) COMPLETED -- Create a JSON file with NFL teams and basic club info
#   2) COMPLETED -- Load the JSON into a dictionary of teams (DOT) at the start of the program
#   3) COMPLETED -- Create a "translate" dictionary that allows conversion of team names to a team KEY
#   4) COMPLETED -- Fill out schedule info in the DOT as we iterate through the page
#   5) COMPLETED -- Write Logic for completed games
#   6) COMPLETED -- Write logic to handle Empty/Missing JSON file
#   7) COMPLETED -- Create a new class to handle creating new JSON info
#   8) COMPLETED -- Modify system to accept a year and create a database for that year
#   10) Refactor code and container-ize as much as possible

# load the season into a dict
def scrapeToJSON(target_year):
    json_target = 'season_'+str(target_year)+'.json'

    try:
        seasonFile = open(json_target)
        dot = json.load(seasonFile)
    except JSONDecodeError:
        print("WARNING: "+json_target+" is unexpectedly empty.")
        print("  - Using empty JSON object instead.")
        dot = json.load(open('league_'+str(target_year)+'.json'))
    except EnvironmentError:
        print("WARNING: "+json_target+" cannot be found.")
        print("  - Creating new JSON file.")
        dot = json.load(open('league_'+str(target_year)+'.json'))

    # load the translate file into a dict
    transFile = open('translate.json')
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
        print('ERROR: Invalid data returned from website. Check URL or try again later.')
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
        if (weekNumber.isnumeric):
            continue

        # second, process all games that still haven't occurred
        if (gameStatus == "pregame"):
            # determine the home and away team keys
            homeTeamKey = translate[columns[5].text.split()[-1].upper()]
            awayTeamKey = translate[columns[3].text.split()[-1].upper()]

            # build two versions of each game to save to both teams' schedules
            homeGame = {
                "opponent"        : awayTeamKey,
                "home-away"       : "Home",
                "day"             : columns[0].text,
                "date"            : columns[1].text,
                "time"            : columns[2].text,
                "status"          : gameStatus
            }

            awayGame = {
                "opponent"        : homeTeamKey,
                "home-away"       : "Away",
                "day"             : columns[0].text,
                "date"            : columns[1].text,
                "time"            : columns[2].text,
                "status"          : gameStatus
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
                    "opp-turnovers"   : int(columns[12].text)
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
                    "opp-turnovers"   : int(columns[10].text)
                }

            else:
                # get home/away team keys
                homeTeamKey = translate[columns[5].text.split()[-1].upper()]
                awayTeamKey = translate[columns[3].text.split()[-1].upper()]

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
                    "opp-turnovers"   : int(columns[10].text)
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
                    "opp-turnovers"   : int(columns[12].text)
                }

        # add this info to each team's dictionary record
        dot[homeTeamKey]["schedule"]["week"+weekNumber] = homeGame
        dot[awayTeamKey]["schedule"]["week"+weekNumber] = awayGame
        
    # output new data back to the season file
    with open(json_target, 'w') as seasonFile:
        new_json = json.dumps(dot, indent=4)
        seasonFile.write(new_json)

    seasonFile.close()

# MAIN CODE EXECUTION BELOW:
scrapeToJSON(2022)
