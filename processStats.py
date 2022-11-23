import numpy as np
import json
from json import JSONDecodeError
from utilities import getTodayInfo

def processStats(dateInfo):
    target_year = dateInfo['season']
    # set a target file for this target ear
    season_target_file = 'data/seasons/'+str(target_year)+'.json'

    seasonFile = open(season_target_file)
    all_teams = json.load(seasonFile)

    # process all weekly stats for saving to "Seasons" database
    print("    Processing Stats for season: "+str(target_year))
    for team in all_teams:
        # set up all stat-variables at zero
        games=wins=losses=ties=points=yards=turnovers=oppPoints=oppYards=oppTurnovers=0

        for week in all_teams[team]["schedule"]:
            if (all_teams[team]["schedule"][week]["status"] == "final"): games += 1
            if (all_teams[team]["schedule"][week]["result"] == "W"): wins += 1
            if (all_teams[team]["schedule"][week]["result"] == "L"): losses += 1
            if (all_teams[team]["schedule"][week]["result"] == "T"): ties += 1
            points += int(all_teams[team]["schedule"][week]["points"])
            yards += int(all_teams[team]["schedule"][week]["yards"])
            turnovers += int(all_teams[team]["schedule"][week]["turnovers"])
            oppPoints += int(all_teams[team]["schedule"][week]["opp-points"])
            oppYards += int(all_teams[team]["schedule"][week]["opp-yards"])
            oppTurnovers += int(all_teams[team]["schedule"][week]["opp-turnovers"])
        
        all_teams[team]["stats"]["games"] = games
        all_teams[team]["stats"]["wins"] = wins
        all_teams[team]["stats"]["losses"] = losses
        all_teams[team]["stats"]["ties"] = ties
        all_teams[team]["stats"]["points"] = points
        all_teams[team]["stats"]["yards"] = yards
        all_teams[team]["stats"]["turnovers"] = turnovers
        all_teams[team]["stats"]["opp-points"] = oppPoints
        all_teams[team]["stats"]["opp-yards"] = oppYards
        all_teams[team]["stats"]["opp-turnovers"] = oppTurnovers
        
        # reset all stat-vars back to zero
        games=wins=losses=ties=points=yards=turnovers=oppPoints=oppYards=oppTurnovers=0

    # output new data back to the season file
    with open(season_target_file, 'w') as seasonFile:
        new_json = json.dumps(all_teams, indent=4)
        seasonFile.write(new_json)

    seasonFile.close()

di = getTodayInfo.getTodayInfo()
processStats(di)