from bs4 import BeautifulSoup
import requests
import json

# GOALS: 
#   1) COMPLETED -- Create a JSON file with NFL teams and basic club info
#   2) COMPLETED -- Load the JSON into a dictionary of teams (DOT) at the start of the program
#   3) COMPLETED -- Create a "translate" dictionary that allows conversion of team names to a team KEY
#   4) Fill out schedule info in the DOT as we iterate through the page

# load the 2022 season into a dict
seasonFile = open('season_2022.json')
dot = json.load(seasonFile)
for team in dot:
    print(dot[team]['location'] + " " + dot[team]['nickname'])

# load the translate file into a dict
transFile = open('translate.json')
translate = json.load(transFile)

# load the 
html_text = requests.get("https://www.pro-football-reference.com/years/2022/games.htm").text
soup = BeautifulSoup(html_text, 'html.parser')

# grab the table from the page for processing
table = soup.find('table').find('tbody')
rows = table.find_all('tr')

# iterate over each row in the table
for row in rows:
    columns = row.find_all('td')
    if len(columns) == 0:
        # The week is finished. Continue to next row and proceed.
        continue
    
    # first, check if the game is concluded...
    gameStatus = "final" if (columns[6].text == "boxscore") else "pregame"

    # second, process the game differently depending on the game status
    if (gameStatus == "pregame"):
        game = {
            "week"            : row.find('th').text,
            "day"             : columns[0].text,
            "date"            : columns[1].text,
            "time"            : columns[2].text,
            "status"          : gameStatus
        }
    


    #### Below Text is useful for reference!!! ####
    # matchup = {
    #     "home"            : columns[3].text,
    #     "away"            : columns[5].text,
    #     "home_points"     : columns[7].text,
    #     "away_points"     : columns[8].text,
    #     "home_yards"      : columns[9].text,
    #     "home_turnovers"  : columns[10].text,
    #     "away_yards"      : columns[11].text,
    #     "away_turnovers"  : columns[12].text,
    # }


    