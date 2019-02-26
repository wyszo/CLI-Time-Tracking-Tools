import os

class LogsWriter: 
    def __init__(self, dirName):
        self.dirName = dirName

    def createLogsDir(self):
        # If logs directory doesn't exist, create it 

        if not os.path.isdir(self.dirName):
            try:
                os.mkdir(self.dirName)
            except:
                print("Warning! Couldn't create \\" + dirName + " directory!")
