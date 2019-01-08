#Author: Scott Degen
#Description: I little library I like to use to organize my python script logging.
#License: MIT https://opensource.org/licenses/MIT
import traceback
import datetime
import time

def LoggerCallback(item):
    Logger.log(item)

class Logger(object):
    errorFile = "errors.log"
    debugFile = "debug.log"
    
    debugWriter = None
    instance = None
    writeLocations = {}
    
    @staticmethod
    def initializeInstance(errorfile, debugfile):
        Logger.instance = Logger(errorfile, debugfile)
    
    @staticmethod
    def log(item):
        
        if Logger.instance:
            Logger.instance.write(item)
        else:
            if isinstance(item, str):   
                print(item)
            else:
                pass
                
    @staticmethod
    def logError(errorWriteable):
        Logger.instance.writeError(errorWriteable)
    
    def __init__(self, errorfile, debugfile):
        self.errorFile = errorfile
        self.debugFile = debugfile
        self.debugWriter = open(debugfile, 'w')
    
    def writeError(self, writeable):
        ts = time.time()
        stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        with open(self.errorFile, 'a') as errorFile:
            errorFile.write("********************\n")
            #todo put time here
            try:
                errorFile.write(stamp + ": " + str(writeable))
            except:
                errorFile.write(stamp + ": Unable to write element.")
            errorFile.write("\n")
            if isinstance(writeable, Exception):
                errorFile.write(stamp + ":\n")
                errorFile.write(traceback.format_exc())
                errorFile.write("\n")
            errorFile.write("********************\n")
    
    def setCase(self, key, deleg):
        self.writeLocations[key] = deleg
    
    def write(self, item):
        ts = time.time()
        if isinstance(item, Exception):
            self.writeError(item)
        
        if isinstance(item, str):
            stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            self.debugWriter.write(stamp + ": " + item + "\n")
            
    def logCase(self, key, value):
        if key in self.writeLocations:
            self.writeLocations[key](value)     
            
        else:
            self.write(value)
            
    def __del__(self):
        self.debugWriter.close()
       