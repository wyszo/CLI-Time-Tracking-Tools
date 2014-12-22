#
# A very simple time tracker. Tracks time spend on a single activity.
# Ruby port 
#

require 'optparse'
require 'io/console'
require 'pp'

$VERSION = 1.05
$elapsedTime = 0


def parseLaunchArguments()
	arguments = {} 

	OptionParser.new do |opts|
		descStr =  "A very simple time tracker. Shows time spend on a single activity.\n"
		scriptFilename = File.basename(__FILE__)
		usageStr = "Usage: " + scriptFilename + " [options]\n"

		opts.banner = descStr + usageStr

		opts.on("-h", "--help", "Displays help") do
			puts opts
			exit
		end

		opts.on("-t", "--time TIME", "Start Time (in minutes or format HH:MM, eg: \'3:23\' or format with \'h\' and \'m\' characters, like \'3h15m\').") do |time|
			pp time
			arguments[:time] = time
		end

		opts.on("-a", "--task TASK", 'Name of the activity which you want to track') do |task|
			pp task
			arguments[:task] = task
		end
	end.parse!

	return arguments
end

def printIntro(version)
	puts ""
	puts "-----------------------------------------"
    puts "A very simple Time Tracking Utility v" + String(version) 
    puts "-----------------------------------------"
    puts ""
end

def grabTaskName(currentTaskName)
	taskName = currentTaskName

	if String(currentTaskName).length == 0
		taskName = ''
		begin 
			print "Enter task name: "
			rawTaskName = gets
			rawTaskName ||= ''
			taskName = rawTaskName.chomp!
			puts ''
		rescue Interrupt
			exit
		end
	end
	return taskName
end

def twoDigitsStringFromNumber(number)
    result = String(number)
    if number < 10
        result = "0" + String(number)
    end
    return result
end

def formattedTime(time)
 	hours = time / 3600
    minutes = (time % 3600) / 60
    seconds = time - hours * 3600 - minutes * 60

    result = twoDigitsStringFromNumber(hours) + ":"
    result += twoDigitsStringFromNumber(minutes) + ":"
    result += twoDigitsStringFromNumber(seconds) 

    return result 
end

def timeStringToInt(timeString)
	if timeString.is_a? Integer
		return timeString
	end
	if timeString.is_a? String
		# TODO: transfer time string -> int conversion from the python script!
		return 0 # stub
	end
end

def startTimeCounter(taskName, elapsedTime) 
	if (not elapsedTime) or (elapsedTime == nil)
		elapsedTime = 0
	end

	$elapsedTime = elapsedTime

	while (true)
		if taskName.length > 0
			print taskName + ' - '
		end
		puts formattedTime($elapsedTime)
		sleep 1
		$elapsedTime += 1
	end
end

def pauseOrAbort()
	begin 
		print "\n/Paused/ - press [enter] to unpause or ^C to quit\n"
		STDIN.noecho(&:gets)
		puts ''
	rescue Interrupt
		puts ''
		exit
	end
end

def main()
	launchArguments = parseLaunchArguments()
	printIntro($VERSION)
	launchArguments[:task] = grabTaskName(launchArguments[:task])
	$elapsedTime = launchArguments[:time]

	while(1)
		begin
			startTimeCounter(launchArguments[:task], $elapsedTime)
		rescue Interrupt
			pauseOrAbort()
		end
	end
end

main()


# TODO: 
# 	1. handling "time" launch argument (converting from string to int and remembering value)
