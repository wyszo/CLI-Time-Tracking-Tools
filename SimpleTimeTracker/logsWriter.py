
import os


class LogsWriter: 
    def __init__(self, dir_name, log_filename):
    	self.log_filename = log_filename
    	self.dir_name = dir_name

    def createLogsDir(self):
        # If logs directory doesn't exist, create it 

        if not os.path.isdir(self.dir_name):
            try:
                os.mkdir(self.dir_name)
            except:
                print("Warning! Couldn't create \\" + dir_name + " directory!")
