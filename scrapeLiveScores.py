from bs4 import BeautifulSoup
from utilities import getTodayInfo
import requests
from populateFirebase import updateFirebase
import json
from json.decoder import JSONDecodeError

#####   ScrapeLiveScores()   #####

def scrapeLiveScores(dateInfo):
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
        # Update if status != "final"
        ref = '/schedules/'+str(dateInfo['season'])+'/'+currWeek+'/'+matchupID+'/'
        updateData = {}
        if jsonMatchup['status'] != 'final':
            if schedJSON[currWeek][matchupID]['status'] == gameState:
                # do nothing
                pass
            else:
                schedJSON[currWeek][matchupID]['status'] = gameState
                # send to firebase...
                updateData['status'] = gameState
                updateFirebase(ref, updateData)
            if gameState == 'pregame':
                lineData = odds.contents[0].split(": ")[1]
                if 'odds' in schedJSON[currWeek][matchupID] and 'date' in schedJSON[currWeek][matchupID]:
                    if schedJSON[currWeek][matchupID]['odds'] == lineData and schedJSON[currWeek][matchupID]['date'] == gameDate:
                        # do nothing
                        pass
                    else:
                        # update schedJSON
                        schedJSON[currWeek][matchupID]['odds'] = lineData
                        schedJSON[currWeek][matchupID]['date'] = gameDate
                        # send to firebase...
                        updateData['odds'] = lineData
                        updateData['date'] = gameDate
                        updateFirebase(ref, updateData)
                else:
                    # update schedJSON
                    schedJSON[currWeek][matchupID]['odds'] = lineData
                    schedJSON[currWeek][matchupID]['date'] = gameDate
                    # send to firebase...
                    updateData['odds'] = lineData
                    updateData['date'] = gameDate
                    updateFirebase(ref, updateData)
            else:
                homeTeamScore = teamScores[1]
                awayTeamScore = teamScores[0]
                if schedJSON[currWeek][matchupID]['score'] == awayTeamScore+"@"+homeTeamScore:
                    # do nothing
                    pass
                else:
                    schedJSON[currWeek][matchupID]['score'] = awayTeamScore+"@"+homeTeamScore
                    # send to firebase...
                    updateData['score'] = awayTeamScore+"@"+homeTeamScore
                    updateFirebase(ref, updateData)

    outputFile = 'data/schedules/'+str(dateInfo['season'])+'.json'
    with open(outputFile, 'w') as outFile:
        new_json = json.dumps(schedJSON, indent=4)
        outFile.write(new_json)