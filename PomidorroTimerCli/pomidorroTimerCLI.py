
import os, sys
import time


def say(text):
	cmd = "echo \"" + str(text) + "\" | espeak -a200 2> /dev/null" # -a: amplitude (volume): <0, 200>
	os.system(cmd)
	

def waitNrOfMin(minutes):
	secsInMinute = 60
	sec = minutes * secsInMinute
	i = 0
	while i < minutes:
			currMin = i
			minLeft = minutes - currMin

			print "... 	[" + str(currMin) + " min, " + str(minLeft) + " left]"

			time.sleep(secsInMinute)
			i = i+1


def currTime():
	currHour = time.strftime('%H')
	currMin = time.strftime('%M')
	currTime = currHour + ":" + currMin
	return currTime


def runPomidorroNr(pomidorroNr):
	pomidorroLen = 25 # minutes
	breakLen = 5 # minutes
	
	helloStr = "Pomidorro #" + str(pomidorroNr) + ": Start [ current time: " + currTime() + " ]" 
	hr = "" + "".join(['-' for i in range(0, len(helloStr))])
	print "\n" + hr
	print helloStr
	print hr + "\n"

	# pomidorro
	waitNrOfMin(pomidorroLen)

	timesUp = "\a\nTime's up, time for a break " 
	print timesUp + " [time: " + str(currTime()) + "]"
	say(timesUp)

	# pormidorro - break
	waitNrOfMin(breakLen)

	back2work = "Back to work"
	print "\a\n" + str(back2work) + " [time: " + str(currTime()) + "]"
	say(back2work)
	raw_input("\nhit [Enter] to start next session")

	return


def pauseOrAbort():
	bQuit = True
	try:
		temp = raw_input('\n\nPress [enter] to restart current session or any other key to quit...\n')

		if temp == '':
			print 'Restarting last session...\n'
			bQuit = False
		else:
			print '\n(exit)'
	except KeyboardInterrupt:
		print '\n(exit)'
	return bQuit


def startSessions(startingNr):
	nr = startingNr
	bQuit = False
	try:
		while 1:
			runPomidorroNr(nr)
			nr = nr+1
	except KeyboardInterrupt:
		bQuit = pauseOrAbort()
	return nr, bQuit
	

def main():
	nr = 1
	bQuit = False
	while not bQuit:
		result = startSessions(nr)
		nr = result[0]
		bQuit = result[1]
			
	return

main()

