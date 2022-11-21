import json

def copy2022Colors(year):
    leagueSourceFile = 'data/leagues/2022.json'
    leagueDestinationFile = 'data/leagues/'+str(year)+'.json'
    seasonDestinationFile = 'data/seasons/'+str(year)+'.json'
    sourceJSON = json.load(open(leagueSourceFile))
    destLeague = json.load(open(leagueDestinationFile))
    destSeason = json.load(open(seasonDestinationFile))

    #Copies color info from source to destination JSON
    for teamKey in sourceJSON:
        if teamKey in destLeague:
            destLeague[teamKey]["colors"] = sourceJSON[teamKey]["colors"]
            destSeason[teamKey]["colors"] = sourceJSON[teamKey]["colors"]
        else:
            # Edge case for OAK => LV switch
            destLeague["OAK"]["colors"] = sourceJSON[teamKey]["colors"]
            destSeason["OAK"]["colors"] = sourceJSON[teamKey]["colors"]
    
    with open(leagueDestinationFile, 'w') as destinationFile:
        new_json = json.dumps(destLeague, indent=4)
        destinationFile.write(new_json)
    destinationFile.close()
    
    with open(seasonDestinationFile, 'w') as destinationFile:
        new_json = json.dumps(destSeason, indent=4)
        destinationFile.write(new_json)
    destinationFile.close()

seasons = [2022]

for season in seasons:
    print("adding IDs for season "+str(season))
    copy2022Colors(season)