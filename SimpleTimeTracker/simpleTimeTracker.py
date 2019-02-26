
import os, sys
import time
import argparse

from logswriter import LogsWriter
from dateformatter import DateFormatter

#
# A very simple time tracker. Tracks time spend on a single activity.
# (I don't know Python well, this script may contain silly code)
#

version = 1.04
timeElapsed = 0
taskName = ''
logsDirName = 'logs'

# -------------------------

def formatAsTwoDigitsStr(nr):
    result = str(nr)
    if nr < 10:
        result = "0" + str(nr)
    return result


def formatTime(inTime):
    hours = inTime/3600
    minutes = (inTime % 3600) / 60
    seconds = inTime - hours * 3600 - minutes * 60

    result = formatAsTwoDigitsStr(hours) + ":"
    result += formatAsTwoDigitsStr(minutes) + ":"
    result += formatAsTwoDigitsStr(seconds) 

    return result 


def countTime(taskName):
    global timeElapsed

    timeStep = 1 # sleeping time

    showTimeInterval = 1 # update printed time info only after # seconds - it is NOT the same as timeStep, don't mix those two
    ctr = 0
    
    while True:
        if ctr % showTimeInterval == 0:
            print taskName + " - " + formatTime(timeElapsed)
        ctr += 1

        time.sleep(timeStep)
        timeElapsed += timeStep
    return

# -------------------------

def pauseOrAbort():
    bQuit = False
    try:
        timeNow = time.strftime("%H:%M", time.localtime())
        inputMsg = "\n/Paused (" + timeNow + ")/ - press [enter] to unpause or ^C to quit\n"
        temp = raw_input(inputMsg)
    except KeyboardInterrupt:
        print
        bQuit = True
    
    print
    return bQuit

# -------------------------

def start():
    global version
    global timeElapsed, taskName

    print '\n-----------------------------------------'
    print 'A very simple Time Tracking Utility v' + str(version)
    print '-----------------------------------------\n'

    if not len(taskName):
        try:
            taskName = raw_input('Enter task name: ')
        except KeyboardInterrupt:
            bQuit = True
            print
            return
        print

    bQuit = False
    while not bQuit:
        try:
            while(1):
                countTime(taskName)
        except KeyboardInterrupt:
            bQuit = pauseOrAbort()

# -------------------------

def printTimeParseError():
    print 'Consult --help for supported time formats!'
    print 'Sorry, defaulting elapsed time to 0!'
    
    
def filterTimeStr(timeStr):
    # remove invalid characters
    allowedChars = ':hm'
    filteredStr = ''.join(c for c in timeStr if c.isdigit() or c in allowedChars)
    
    # convert format HH'h'MM'm', convert to hh:mm
    str = filteredStr
    str = str.replace('h', ':')
    str = str.replace('m', '')
    
    return str
    

def setupStartTime(timeStr):
    global timeElapsed
    
    # character validation & filtering
    if timeStr == 0:
        return
    
    timeStr = filterTimeStr(timeStr)
        
    # problably simple integer value
    if timeStr.find(':') == -1:
        try:
            intTime = int(timeStr) 
            timeElapsed = intTime * 60 # convert value to # of minutes
        except ValueError:
            print 'Error: unknown time format!'
            printTimeParseError()
            return
    # probably format hh:mm    
    else:
        time = timeStr.split(':')
        
        # check for unsupported characters # obsolete - done during filtering
        for c in timeStr:
            if c.isdigit() == False and c != ':': 
                print ("Error: unknown time format! Unsupported character: '" + c + "'")
                printTimeParseError()
                return
    
        # validate time array length and element types
        if len(time) > 2 or (time[0].isdigit() == False) or (time[1].isdigit() == False):
            print "Error: unknown time format!"
            printTimeParseError()
            return
        
        # everything seems fine, set elapsed time
        try:
            hours = int(time[0])
            minutes = int(time[1])
        except ValueError:
            print 'Error: unknown time format!'
            printTimeParseError()
            return
        
        timeElapsed = hours * 3600 + minutes * 60

# -------------------------

def parseArgs():
    global timeElapsed, taskName
    
    # prepare arg parser
    descStr = "A very simple time tracker. Shows time spend on a single activity."
    parser = argparse.ArgumentParser(description = descStr)
    
    parser.add_argument('--time', metavar='StartTime', default=0, type=str, help='Start Time (in minutes or format HH:MM, eg: \'3:23\' or format with \'h\' and \'m\' characters, like \'3h15m\').')
    parser.add_argument('--task', metavar='TaskName', type=str, help='Name of the activity which you want to track')
    
    # parse & handle args
    args = parser.parse_args()
    setupStartTime(args.time)
    taskName = args.task
    if not taskName:
        taskName = ''
    return

# -------------------------

def main():
    today = DateFormatter().today()

    writer = LogsWriter(logsDirName, today)
    writer.createLogsDir()

    parseArgs()
    start()
    return

# -------------------------

main()
