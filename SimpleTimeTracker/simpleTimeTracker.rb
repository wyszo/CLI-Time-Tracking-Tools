#
# A very simple time tracker. Tracks time spend on a single activity.
# Ruby port 
#

require 'optparse'
require 'pp'


version = 1.05


def printVersion(version)
	print "hello!\n"
	print "version " + String(version)
end


OptionParser.new do |opts|
	descStr =  "A very simple time tracker. Shows time spend on a single activity.\n"
	scriptFilename = File.basename(__FILE__)
	usageStr = "Usage: " + scriptFilename + " [options]\n"

	opts.banner = descStr + usageStr

	opts.on("-h", "--help", "Displays help") do
		puts opts
		exit
	end
end.parse!


printVersion(version)
