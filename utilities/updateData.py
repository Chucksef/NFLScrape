import json

def updateData(file, ref, newData):
    seasonFile = open('data/'+file)
    old_json = json.load(seasonFile)

    # strip ref of leading/trailing "/"
    ref = ref.strip("/")
    
    # parse ref
    refParts = ref.split("/")

    # update old json
    if len(refParts) == 10: old_json[refParts[0]][refParts[1]][refParts[2]][refParts[3]][refParts[4]][refParts[5]][refParts[6]][refParts[7]][refParts[8]][refParts[9]] = newData
    if len(refParts)  == 9: old_json[refParts[0]][refParts[1]][refParts[2]][refParts[3]][refParts[4]][refParts[5]][refParts[6]][refParts[7]][refParts[8]] = newData
    if len(refParts)  == 8: old_json[refParts[0]][refParts[1]][refParts[2]][refParts[3]][refParts[4]][refParts[5]][refParts[6]][refParts[7]] = newData
    if len(refParts)  == 7: old_json[refParts[0]][refParts[1]][refParts[2]][refParts[3]][refParts[4]][refParts[5]][refParts[6]] = newData
    if len(refParts)  == 6: old_json[refParts[0]][refParts[1]][refParts[2]][refParts[3]][refParts[4]][refParts[5]] = newData
    if len(refParts)  == 5: old_json[refParts[0]][refParts[1]][refParts[2]][refParts[3]][refParts[4]] = newData
    if len(refParts)  == 4: old_json[refParts[0]][refParts[1]][refParts[2]][refParts[3]] = newData
    if len(refParts)  == 3: old_json[refParts[0]][refParts[1]][refParts[2]] = newData
    if len(refParts)  == 2: old_json[refParts[0]][refParts[1]] = newData
    if len(refParts)  == 1: old_json[refParts[0]] = newData

    with open('data/'+file, 'w') as f:
        new_json = json.dumps(old_json, indent=4)
        f.write(new_json)
        f.close()