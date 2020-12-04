#!/usr/bin/env python

import os, sys, subprocess, time, argparse

#
# Pomodoro Technique Command Line script
# (google it or visit http://pomodorotechnique.com/ )
#

pomodoroLengthMinutes = 25
breakLengthMinutes = 5

# -------------------------

def add_shared_dir_to_path():
    import os, sys

    current_dir = os.path.dirname(__file__)
    shared_dir = os.path.join(current_dir, '../Shared')
    sys.path.append(shared_dir)

# -------------------------

def cmdExists(cmd):
    return subprocess.call(["command", "-v", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

def say(text):
    cmd = ""

    if cmdExists("espeak"):
        cmd = "echo \"" + str(text) + "\" | espeak -a200 2> /dev/null" # -a: amplitude (volume): <0, 200>
    else:
        if cmdExists("say"):
            cmd = "echo \"" + str(text) + "\" | say 2> /dev/null"

    if cmd:
        os.system(cmd)

# -------------------------

def waitNrOfMin(minutes):
    add_shared_dir_to_path()
    import shared

    secsInMinute = 60
    sec = minutes * secsInMinute
    i = 0
    while i < minutes:
        currMin = i
        minLeft = minutes - currMin

        shared.print_inline("...    [" + str(currMin) + " min, " + str(minLeft) + " left]")

        time.sleep(secsInMinute)
        i = i+1

# -------------------------

def currentTime():
    currentHour = time.strftime('%H')
    currentMin = time.strftime('%M')
    currentTime = currentHour + ":" + currentMin
    return currentTime

# -------------------------

def runPomodoroNr(pomodoroNr):
    global pomodoroLengthMinutes

    helloStr = "Pomodoro #" + str(pomodoroNr) + ": Start [ current time: " + currentTime() + " ]"
    hr = "" + "".join(['-' for i in range(0, len(helloStr))])
    print "\n" + hr
    print helloStr
    print hr + "\n"

    # pomodoro
    waitNrOfMin(pomodoroLengthMinutes)

    timesUp = "\a\nTime's up, time for a break "
    print timesUp + " [time: " + str(currentTime()) + "]"
    say(timesUp)


def runBreak():
    global breakLengthMinutes

    waitNrOfMin(breakLengthMinutes)

    back2work = "Back to work"
    print "\a\n" + str(back2work) + " [time: " + str(currentTime()) + "]"
    say(back2work)
    raw_input("\nhit [Enter] to start next session")

# -------------------------

def pauseOrAbort(message, enterPressedMessage):
    bQuit = True
    try:
        temp = raw_input('\n\n' + message + '\n')

        if temp == '':
            print (enterPressedMessage + '\n')
            bQuit = False
        else:
            print
    except KeyboardInterrupt:
        print
    return bQuit

# -------------------------

def startSessions(startingNr):
    nr = startingNr
    bQuit = False

    while 1:
        try:
            runPomodoroNr(nr)
            nr = nr+1

            try:
                runBreak()
            except KeyboardInterrupt:
                bQuit = pauseOrAbort("Press [enter] to end break and start next session or any other key to quit...", "Starting next session...")
                if bQuit:
                    break
        except KeyboardInterrupt:
            bQuit = pauseOrAbort("Press [enter] to restart current session or any other key to quit...", "Restarting last session...")
            break

    return nr, bQuit

# -------------------------

def nextSessionNumberFromCliArgs():
    descStr = "Command line utility for 'Pomodoro technique' (google it up or visit http://pomodorotechnique.com/)"
    parser = argparse.ArgumentParser(description = descStr)

    parser.add_argument('--start_from',
                        metavar='StartFromNr',
                        default=1,
                        type=int,
                        help='first pomodoro session number (default: 1)')

    #parse arguments
    arguments = parser.parse_args()
    nextSessionNumber = arguments.start_from
    return nextSessionNumber

# -------------------------

def main():
    nextSessionNumber = nextSessionNumberFromCliArgs()
    add_shared_dir_to_path()
    import shared, version, settings
    shared.print_version(settings.printable_script_name, version.version)

    bQuit = False
    while not bQuit:
        result = startSessions(nextSessionNumber)
        nextSessionNumber = result[0]
        bQuit = result[1]

    return

main()

