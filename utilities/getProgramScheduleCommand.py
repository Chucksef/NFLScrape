def getProgramScheduleCommand(currTimeStr):
    schedFile = open('programSchedule.txt', 'r')
    schedLines = schedFile.readlines()
    schedFile.close()

    # temp array to use to write later
    writeLines = schedLines.copy()
    output = ''
    schedTimeStr = ''

    for line in schedLines:
        if line[0] == "#":
            # remove line from array
            writeLines.pop(0)
            continue
        elif line[0] == "$":
            output = None
            break
        else:
            writeLines.pop(0)
            output = line.split("---")[1].strip()
            schedTimeStr = line.split("---")[0]
            break
    
    # check if it is after the scheduled time
    if output != '':
        if int(currTimeStr) > int(schedTimeStr):
            # write out lines
            outputFile = 'programSchedule.txt'
            with open(outputFile, 'w') as outFile:
                for line in writeLines:
                    outFile.write(f"{line}")

            return output
        else:
            print("    curr: "+currTimeStr)
            print("    schd: "+schedTimeStr)
            return 'nothingScheduledYet'
    else:
        return 'noOutputFound'

    