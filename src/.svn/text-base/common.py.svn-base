
__author__="jeffrey"
__date__ ="$Mar 13, 2009 9:06:13 PM$"

import os
import ConfigParser
import random
from time import strptime,sleep
from Queue import Queue
import pytz
import yaml

class WebError(Exception): pass
class BotError(Exception): pass
class BotFatalError (BotError): pass
class ManuallyTerminated(BotError): pass
class FleetSendError(BotError): pass
class FleetLaunchAbortedError(FleetSendError): pass
class NoFreeSlotsError(FleetSendError):
    def __str__(self): return "No fleet slots available"
class NotEnoughShipsError (FleetSendError):
    def __init__(self,allFleetAvailable,requested,available = None):
        self.allFleetAvailable = allFleetAvailable
        self.requested = requested
        self.available = available
    def __str__(self):
        return 'Requested: %s. Available: %s' %(self.requested,self.available)
    
def my_sleep(seconds):
    for dummy in range(0, random.randrange(seconds, seconds+10)):
        sleep(1)


de_timezone = pytz.timezone(pytz.country_timezones['de'][0])

class Configuration(dict):
    def __init__(self, file):
        config = yaml.load(file.read())
        file.close()
        self.update(config)

    def __getattr__(self, attr):
        return self[attr]

class Translations(dict):
    def __init__(self):

        for fileName in os.listdir(os.getcwd() + '/languages'):
            fileName, extension = os.path.splitext(fileName)

            if not fileName or fileName.startswith('.') or extension != '.ini':
                continue
            parser = ConfigParser.SafeConfigParser()
            parser.optionxform = str # prevent ini parser from converting names to lowercase
            try:
                #file = codecs.open('languages/'+fileName+extension, "r", "utf-8" ) # language files are codified in UTF-8
                parser.read('languages/'+fileName+extension)
                translation = {}
                for section in parser.sections():
                	translation.update((key, value) for key, value in parser.items(section))
                self[translation['languageCode']] = translation
            except Exception, e:
                raise BotError("Malformed language file (%s%s): %s"%(fileName,extension,e))

class Enum(object):
    @classmethod
    def toStr(self, type):
        return [i for i in self.__dict__ if getattr(self, i) == type][0]