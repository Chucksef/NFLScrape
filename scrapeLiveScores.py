from bs4 import BeautifulSoup
from utilities import getTodayInfo
import requests
import json
from json.decoder import JSONDecodeError

#####   scrapeToJSON()   #####
#####        INFO        #####
# This program does the main scraping process for getting NFL data from pro-football-reference.com and saves it into "season_XXXX.json" files.
# This program is nominally callable from outside of itself. Users or programs should call it using the name scrapeToJSON(XXXX), where XXXX is
# the year for the data that is being requested. Not all years are expected to work out of the box. No year can be scraped without a 
# "league_XXXX.json" file located inside of the data folder. This file sets up each team's keyName and sets up a variety of other data.



def scrapeLiveScores():
    # get today
    dateInfo = getTodayInfo.getTodayInfo()
    currWeek = dateInfo['weekID'].split("-")[1]

    # open the schedule for comparison
    schedule_target_file = 'data/schedules/'+str(dateInfo['season'])+'.json'
    seasonFile = open(schedule_target_file)
    schedJSON = json.load(seasonFile)

    # load the translate file into a dict
    transFile = open('data/translates/'+str(dateInfo['season'])+'.json')
    translate = json.load(transFile)
    transFile.close()

    # load the target webpage for scraping
    target_website = "https://www.espn.com/nfl/scoreboard"
    html_text = requests.get(target_website).text
    soup = BeautifulSoup(html_text, 'html.parser')
    body = soup.find('body')
    # Get an array of all instances of 'section.Scoreboard'
    matchups = body.find_all("section", class_="Scoreboard")
    # Iterate over them:
    for matchup in matchups:
        # Get nearest Header parent to determine day of week / time of play
        tempParent = matchup.parent.previousSibling
        gameDate = tempParent.get('aria-label')
        # Construct MatchupID
        matchupID = currWeek+"-"
        # Check for existence of "Highlights" button:
        gameState = ""
        highlights = matchup.find('a', text='Highlights')
        if (highlights):
            # If it does, then this game is final
            gameState = "final"
        else:
            # Check for existence of 'div.Odds__Message'
            odds = matchup.find('div', class_="Odds__Message")
            if (odds):
                # If it exists, game is pregame
                gameState = "pregame"
            else:
                # If it doesn't, game is ongoing
                gameState = "live"
        print(gameState+" game:")
        # Get the contents of div.ScoreCell__TeamName => each team's name
        teamNames = [tn.text for tn in matchup.find_all("div", class_="ScoreCell__TeamName")]
        # Get the contents of div.ScoreCell__Score => each team's score
        teamScores = [tn.text for tn in matchup.find_all("div", class_="ScoreCell__Score")]
        # Translate these team names for data-conformity and build he matchupID
        homeTeamKey = translate[teamNames[1].upper()]
        awayTeamKey = translate[teamNames[0].upper()]
        matchupID += awayTeamKey+"@"+homeTeamKey
        # Look up the game status in the schedJSON
        jsonMatchup = schedJSON[currWeek][matchupID]
        print(jsonMatchup)
        # Update if status != "final"
        if jsonMatchup['status'] != 'final':
            schedJSON[currWeek][matchupID]['status'] = gameState
            if gameState == 'pregame':
                schedJSON[currWeek][matchupID]['odds'] = odds.text
                schedJSON[currWeek][matchupID]['date'] = gameDate
            else:
                homeTeamScore = teamScores[1]
                awayTeamScore = teamScores[0]
                schedJSON[currWeek][matchupID]['score'] = awayTeamScore+"@"+homeTeamScore
                # If so, also write out to Firebase
    print(schedJSON)
        
    # 
        

    # outputFile = 'schedules/dateInfo['season'].json'
    # with open(outputFile, 'w') as outFile:
    #     new_json = json.dumps(schedJSON, indent=4)
    #     outFile.write(new_json)

scrapeLiveScores()