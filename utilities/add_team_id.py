import json

def addTeamId(year):
    seasonTargetFile = 'data/leagues/'+str(year)+'.json'
    seasonJSON = json.load(open(seasonTargetFile))
    for teamKey in seasonJSON:
        teamID = "team-"+teamKey+str(year)
        seasonJSON[teamKey]["id"] = teamID
    
    with open(seasonTargetFile, 'w') as seasonFile:
        new_json = json.dumps(seasonJSON, indent=4)
        seasonFile.write(new_json)
    
    seasonFile.close()

seasons = [2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002]

for season in seasons:
    print("adding IDs for season "+str(season))
    addTeamId(season)