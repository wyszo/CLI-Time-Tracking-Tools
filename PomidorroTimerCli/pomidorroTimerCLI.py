
import os, sys, subprocess, time, argparse

#
# A very simple cli utility for 'Pomidorro technique' (google it up)
# (I don't know Python well, this script may contain silly code)
#

version = 1.01
pomidorroLen = 25 # minutes
breakLen = 5 # minutes

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
	secsInMinute = 60
	sec = minutes * secsInMinute
	i = 0
	while i < minutes:
		currMin = i
		minLeft = minutes - currMin

		print "... 	[" + str(currMin) + " min, " + str(minLeft) + " left]"

		time.sleep(secsInMinute)
		i = i+1

# -------------------------

def currTime():
	currHour = time.strftime('%H')
	currMin = time.strftime('%M')
	currTime = currHour + ":" + currMin
	return currTime

# -------------------------

def runPomidorroNr(pomidorroNr):
	global pomidorroLen
	
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


def runBreak():
	global breakLen
	
	waitNrOfMin(breakLen)

	back2work = "Back to work"
	print "\a\n" + str(back2work) + " [time: " + str(currTime()) + "]"
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
			runPomidorroNr(nr)
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

def startNrFromCliArgs():
	descStr = "A very simple CLI utility for 'Pomidorro technique' (google it up)"
	parser = argparse.ArgumentParser(description = descStr)
	
	parser.add_argument('--start_from', metavar='StartFromNr', default=1, type=int, help='Start counting pomidorro sessions from this number (defaults to 1)')
	
	#parse args
	args = parser.parse_args()
	startNr = args.start_from
	return startNr

# -------------------------

def main():
	startNr = startNrFromCliArgs()
	print '\nPomidorro Timer CLI Utility v' + str(version)
	
	bQuit = False
	while not bQuit:
		result = startSessions(startNr)
		startNr = result[0]
		bQuit = result[1]
			
	return

main()

