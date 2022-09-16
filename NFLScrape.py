from bs4 import BeautifulSoup
import requests

html_text = requests.get("https://www.pro-football-reference.com/years/2022/games.htm").text
soup = BeautifulSoup(html_text, 'html.parser')

table = soup.find('table').find('tbody')
rows = table.find_all('tr')

#iterate over each row on the page
for idx, row in enumerate(rows):
    week_number = row.find('th').text
    columns = row.find_all('td')
    day = columns[0].text
    date = columns[1].text
    time = columns[2].text
    winner = columns[3].text
    homeaway = "away" if (columns[4].text == "@") else "home"
    loser = columns[5].text
    status = columns[6].text
    winner_points = columns[7].text
    lower_points = columns[8].text
    winner_yards = columns[9].text
    winner_turnovers = columns[10].text
    loser_yards = columns[11].text
    loser_turnovers = columns[12].text


    