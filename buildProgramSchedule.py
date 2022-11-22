from populateFirebase import updateWeek
from utilities import getTodayInfo
from scrapeLiveScores import scrapeLiveScores

# Weekly Schedule:
# Tuesday @ 3:30am buildProgramSchedule will be run as the last scheduled event from the previous week
# It will run and programSchedule.txt will be filled out with schedule information

### Program Execution:
def buildProgramSchedule(dateInfo):
    #   directly call updateWeek() to enable picking for the next week's games.
    updateWeek(dateInfo)
    scrapeLiveScores(dateInfo)

    #   Second, schedule scrapeLiveScores() every 2 hours beginning at 4am Tuesday and ending at 5 min before kickoff of the first game
    #   Third, schedule updateWeek() to be called 1 min after the start of the first game this week
    #   Read NFL Schedule and create 15-second interval scrapeLiveScores calls for each game-window

di = getTodayInfo.getTodayInfo()
buildProgramSchedule(di)