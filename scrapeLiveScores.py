from bs4 import BeautifulSoup
from utilities.getTodayInfo import getTodayInfo
from populateFirebase import updateFirebase
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class MyBot:
    def __init__(self):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"

        self.sv = Service('/usr/bin/chromedriver')

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
            service=self.sv, # FOR LINUX
            #executable_path='chromedriver107.exe', # FOR WINDOWS
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

    # get lowest value of all dates/times in schedule
    gameTimes = [int(schedJSON[currWeek][d]['date']+schedJSON[currWeek][d]['time']) for d in schedJSON[currWeek]]
    firstGameStartTime = min(gameTimes)

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
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find('body')

    # Get an array of all instances of 'section.Scoreboard'
    matchups = body.find_all("section", class_="Scoreboard")
    # Iterate over them:
    for matchup in matchups:
        # Construct MatchupID
        matchupID = currWeek+"-"
        odds = None
        # Get the state of the game: "pregame", "final", or "live"
        gameState = ""
        timeCell = matchup.find('div', class_='ScoreCell__Time')
        timeStatus = timeCell.text
        if timeStatus == "Final":
            gameState = 'final'
        elif 'PM' in timeStatus or 'AM' in timeStatus:
            gameState = 'pregame'
            odds = matchup.find('div', class_="Odds__Message")
        else:
            gameState = 'live'
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
                lineData = odds.contents[0].split(": ")[1] if odds else None
                if lineData and schedJSON[currWeek][matchupID]['odds'] != lineData:
                    # Only update odds if the first game hasn't started yet
                    if (int(dateInfo['timestr'][:-2]) > firstGameStartTime):
                        pass        # do nothing...
                    else:
                        # update schedJSON for pregame game
                        schedJSON[currWeek][matchupID]['odds'] = lineData
                        # send to firebase...
                        updateData['odds'] = lineData
                        updateFirebase(ref, updateData)
            elif gameState == 'live':
                homeTeamScore = teamScores[1]
                awayTeamScore = teamScores[0]
                # UPDATE SCORES
                # only update scores if the live score is different than the JSON score
                if schedJSON[currWeek][matchupID]['score'] == awayTeamScore+"@"+homeTeamScore:
                    # do nothing
                    pass
                else:
                    schedJSON[currWeek][matchupID]['score'] = awayTeamScore+"@"+homeTeamScore
                    # send to firebase...
                    updateData['score'] = awayTeamScore+"@"+homeTeamScore
                    updateFirebase(ref, updateData)
                # UPDATE STATUS
                # only update game status if the live status is different than the JSON status
                if schedJSON[currWeek][matchupID]['status'] == timeStatus:
                    # do nothing
                    pass
                else:
                    schedJSON[currWeek][matchupID]['status'] = timeStatus
                    # send to firebase...
                    updateData['status'] = timeStatus
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

di = getTodayInfo()
scrapeLiveScores(di)