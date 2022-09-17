from bs4 import BeautifulSoup
import requests
import json

html_text = requests.get("https://www.pro-football-reference.com/years/2022/games.htm").text
soup = BeautifulSoup(html_text, 'html.parser')

# grab the table from the page for processing
table = soup.find('table').find('tbody')
rows = table.find_all('tr')

# we want to build a json object as we iterate and eventually save it out to a file


# iterate over each row in the table
for idx, row in enumerate(rows):
    columns = row.find_all('td')
    if len(columns) == 0:
        continue
    
    matchup = {
        "week"            : row.find('th').text,
        "day"             : columns[0].text,
        "date"            : columns[1].text,
        "time"            : columns[2].text,
        "home"            : columns[3].text,
        "away"            : columns[5].text,
        "home_points"     : columns[7].text,
        "away_points"     : columns[8].text,
        "home_yards"      : columns[9].text,
        "home_turnovers"  : columns[10].text,
        "away_yards"      : columns[11].text,
        "away_turnovers"  : columns[12].text,
    }


    