from bs4 import BeautifulSoup
from utilities import getTodayInfo
import requests
from populateFirebase import updateFirebase
import json
from selenium import webdriver

from json.decoder import JSONDecodeError


class MyBot:
    def __init__(self):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"

        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        self.options.add_argument(f'user-agent={user_agent}')
        self.options.add_argument('--window-size=1920,1080')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--allow-running-insecure-content')
        self.options.add_argument('--diable-extensions')
        self.options.add_argument('--proxy-server="direct://"')
        self.options.add_argument('--proxy-bypass-list=*')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(
            executable_path='chromedriver.exe',
            options=self.options)

#####   ScrapeLiveScores()   #####

def scrapeLiveScores(dateInfo):
    season = dateInfo['season']

    # open the schedule for comparison
    schedule_target_file = 'data/schedules/'+str(season)+'.json'
    seasonFile = open(schedule_target_file)
    schedJSON = json.load(seasonFile)

    # get current week from schedule
    currWeek = schedJSON['status']['currentWeek'].split("-")[1]
    currWeekNum = int(currWeek.replace("week",''))

    # load the translate file into a dict
    transFile = open('data/translates/'+str(dateInfo['season'])+'.json')
    translate = json.load(transFile)
    transFile.close()

    # load the target webpage for scraping
    target_website = "https://www.espn.com/nfl/scoreboard/_/week/"+str(currWeekNum)+"/year/"+str(season)+"/seasontype/2"
    browser = MyBot()
    browser.driver.get(target_website)
    html = browser.driver.page_source
    browser.driver.close()
    # html_text = requests.get(target_website).text
    soup = BeautifulSoup(html, 'html.parser')
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
        watchButton = matchup.find('section', class_='DriveChart2D')
        if watchButton:
            # If it does, then this game is final
            gameState = "live"
        else:
            # Check for existence of 'div.Odds__Message'
            odds = matchup.find('div', class_="Odds__Message")
            if (odds):
                # If it exists, game is pregame
                gameState = "pregame"
            else:
                # If it doesn't, game is ongoing
                gameState = "final"
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
        if jsonMatchup['status'] != 'final':
            updateData = {}
            if gameState == 'pregame':
                lineData = odds.contents[0].split(": ")[1]
                if 'odds' in schedJSON[currWeek][matchupID] and 'date' in schedJSON[currWeek][matchupID]:
                    if schedJSON[currWeek][matchupID]['odds'] == lineData and schedJSON[currWeek][matchupID]['date'] == gameDate:
                        # do nothing
                        pass
                    else:
                        # if (past Thursday at 6:30pm):                        <========todo
                            # pass
                        # else: (below block)
                        # update schedJSON for pregame game
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
            elif gameState == 'live':
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
            else:
                # gamestate = final
                homeTeamScore = teamScores[1]
                awayTeamScore = teamScores[0]
                schedJSON[currWeek][matchupID]['score'] = awayTeamScore+"@"+homeTeamScore
                # send to firebase...
                updateData['score'] = awayTeamScore+"@"+homeTeamScore
                updateFirebase(ref, updateData)


    outputFile = 'data/schedules/'+str(dateInfo['season'])+'.json'
    with open(outputFile, 'w') as outFile:
        new_json = json.dumps(schedJSON, indent=4)
        outFile.write(new_json)

di = getTodayInfo.getTodayInfo()
scrapeLiveScores(di)