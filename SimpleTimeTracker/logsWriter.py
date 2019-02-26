import os
from datetime import date

class LogsWriter: 
    def __init__(self, dir_name):
    	self.today = DateFormatter().today()
    	self.dir_name = dir_name

    def createLogsDir(self):
        # If logs directory doesn't exist, create it 

        if not os.path.isdir(self.dir_name):
            try:
                os.mkdir(self.dir_name)
            except:
                print("Warning! Couldn't create \\" + dir_name + " directory!")


class DateFormatter:
	def today(self):
		return str(date.today())
