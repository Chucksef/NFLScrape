def getProgramScheduleCommand(currTimeStr):
    schedFile = open('programSchedule.txt', 'r')
    schedLines = schedFile.readlines()
    schedFile.close()

    # temp array to use to write later
    writeLines = schedLines.copy()
    command = ''
    argument = ''
    schedTimeStr = ''

    for line in schedLines:
        if line[0] == "#":
            # remove line from array
            writeLines.pop(0)
            continue
        elif line[0] == "$":
            command = None
            argument = None
            break
        else:
            writeLines.pop(0)
            command = line.split("---")[1].strip()
            if " " in command:
                (command, argument) = command.split(" ")
            else:
                argument = None
            schedTimeStr = line.split("---")[0]
            break
    
    # check if it is after the scheduled time
    if command != '':
        if int(currTimeStr) > int(schedTimeStr):
            # write out lines
            outputFile = 'programSchedule.txt'
            with open(outputFile, 'w') as outFile:
                for line in writeLines:
                    outFile.write(f"{line}")

            return (command, (argument == 'True'))
        else:
            return ('nothingScheduledYet', None)
    else:
        return ('noOutputFound', None)

    