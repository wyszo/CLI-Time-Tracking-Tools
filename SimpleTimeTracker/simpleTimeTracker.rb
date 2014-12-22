#
# A very simple time tracker. Tracks time spend on a single activity.
# Ruby port 
#

require 'optparse'
require 'pp'


$VERSION = 1.05


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
			puts "Enter task name: "
			rawTaskName = gets
			rawTaskName ||= ''
			taskName = rawTaskName.chomp!
		rescue Interrupt
			exit
		end
	end
	return taskName
end


def main()
	launchArguments = parseLaunchArguments()
	printIntro($VERSION)
	launchArguments[:task] = grabTaskName(launchArguments[:task])
end


main()


# 2. enter task name (if not present)
