#!/Library/Frameworks/Python.framework/Versions/3.11/bin/python3
import subprocess
import requests
import logging
import os
import psutil
import sys
import re
import Foundation
import objc
import math
import time
from getpass import getuser

# Logging
robloxLogs = f"/Users/{getuser()}/Library/Logs/Roblox/"
class MainLogger:
    def __init__(self, filename):
        self._streamHandler = logging.StreamHandler()
        self._fileHandler = logging.FileHandler(filename)
        self._formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        self.logger = logging.getLogger(__name__)
        self.logger.propagate = False
        self.logger.setLevel(logging.DEBUG)

        self._streamHandler.setFormatter(self._formatter)
        self._fileHandler.setFormatter(self._formatter)
        self.logger.addHandler(self._streamHandler)
        self.logger.addHandler(self._fileHandler)

# Monitor stuff
running = True

NSUserNotification = objc.lookUpClass('NSUserNotification')
NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
def notify(title, text):
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(text)
    notification.setUserInfo_({})
    notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(0, Foundation.NSDate.date()))
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)
    
def isRobloxRunning(txt : str = ""):
    if "FLog::SingleSurfaceApp] destroyLuaApp: (stage:LuaApp)... finished destroying luaApp." in txt:
        return False
    for app in psutil.process_iter():
        try:
            name = app.name()
            if "OldRobloxPlayer" in name:
                return True
            elif "--debug" in sys.argv and "RobloxPlayer" in name:
                return True
        except psutil.NoSuchProcess:
            return False
    return False
def executeString(capturedLine : str, logger : logging.Logger):
    if "[FLog::Output] ! Joining game" in capturedLine:
        global gamename
        global gamecreator
        # I dont really know how to make regex patterns
        gameid = capturedLine.split()[7]
        universeIdHTTP = f"https://apis.roblox.com/universes/v1/places/{gameid}/universe"
        logger.info(f"GET Request to {universeIdHTTP}")
        universeId = requests.get(universeIdHTTP)
        logger.info(f"Server returned {universeId.status_code}\n{universeId.text}")
        universeid = universeId.json()["universeId"]
        if universeId == None:
            logger.error("Server returned Universe ID as None!!")
            return
        
        gameInfoHTTP = f"https://games.roblox.com/v1/games?universeIds={universeid}"
        logger.info(f"GET Request to {gameInfoHTTP}")
        gameInfo = requests.get(gameInfoHTTP)
        logger.info(f"Server returned {gameInfo.status_code}\n{gameInfo.text}")
        gameInfo = gameInfo.json()["data"]
        if len(gameInfo) == 0:
            logging.error("Server didnt return any data!!")
            return
        gamename = gameInfo[0]["name"]
        gamecreator = gameInfo[0]["creator"]["name"]
        logging.info(f"The Game ID {gameid} is {gamename} by {gamecreator}")
    elif "[FLog::Network] UDMUX Address" in capturedLine:
        # https://github.com/pizzaboxer/bloxstrap/blob/main/Bloxstrap/Integrations/ActivityWatcher.cs
        searchedIP = re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", capturedLine)
        searchedIP = capturedLine.split()[5][:-1]
        if searchedIP:
            serverip = searchedIP
            logger.info(f"Catched server's IP address: {serverip}")
            logger.info("Finding the location of the IP address")
            requestInfo = requests.get(f"https://ipinfo.io/{serverip}/json")
            logger.info(f"Server returned {requestInfo.status_code}\n{requestInfo.text}")
            requestInfo = requestInfo.json()
            location = ""
            if requestInfo["city"] == requestInfo["region"]:
                location = f"{requestInfo['region']}, {requestInfo['country']}"
            else:
                location = f"{requestInfo['city']}, {requestInfo['region']}, {requestInfo['country']}"
            notify(f"Joining {gamename} by {gamecreator}", f"Located at {location}")
            logger.info(f"Server is located at {location}")
    elif "[FLog::Network] Time to disconnect replication data:" in capturedLine:
        logger.info("Leaving")
failsafe = False
logger = MainLogger(os.path.join(robloxLogs, f"RobloxServerTracker_{math.floor(time.time())}.log")).logger
logger.info(f"PID: {os.getpid()}")
os.chdir("/Applications/Roblox.app/Contents/MacOS")
try:
    with subprocess.Popen(["/Applications/Roblox.app/Contents/MacOS/./OldRobloxPlayer"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as rblxproc:
        logger.info(f"Roblox PID {rblxproc.pid}")
        while not failsafe:
            capturedLine = rblxproc.stdout.readline().decode(errors="ignore")
            if not isRobloxRunning(capturedLine) or rblxproc.poll():
                logger.info("Roblox is not running, exiting.")
                rblxproc.kill()
                sys.exit()
            #print(rblxproc.poll(), end="\r")
            executeString(capturedLine, logger)
except KeyboardInterrupt:
    # If ran manually
    logger.info("Quitting")
    failsafe = True
    sys.exit()
