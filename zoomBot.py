# By Nathaniel Louis Tisuela
from flask import Flask, request
import requests
import json
import base64
import time
import threading
from zoomWrapper import ZoomWrapper
import atexit

app = Flask(__name__)
zoomBot = None
commonData = {}
dataLock = threading.Lock()
backgroundThread = threading.Thread()
# "292922e53c6e4e328e79d2fc9a918653"

class ZoomBot:

    def __init__(self):
        self.waitTime = 5
        self.logFileName = "logs.txt"
        self.zoom = ZoomWrapper()

        watchChannelNames = ["teest"]
        self.watchChannels = self.initWatchChannels(watchChannelNames)

        # for multithreading
        self.initBackgroundLoop()
        atexit.register(self.interrupt)



    def getChannel(self, name: str):
        ''' Search channels by name
        '''
        for channel in self.zoom.getChannels()["channels"]:
            if channel["name"] == name:
                return channel

        # if none return empty dict
        return dict()



    def initWatchChannels(self, names):
        ''' Initialize the list of channels to read from
        '''
        result = []

        for name in names:
            channel = self.getChannel(name)

            # ensure channel exists
            if (len(channel) > 0):
                result.append(channel)

        return result


    def getMessages(self):
        messages = []
        for channel in self.watchChannels:
            channelMessages = self.zoom.getChannelMessages(channel["id"])["messages"]

            for message in channelMessages:
                if self.isNewMessage(message):
                    message["channel_id"] = channel["id"]
                    self.logMessage(message)
                    messages.append(message)

        return messages



    def logMessage(self, message: dict):
        with open(self.logFileName, "a+") as logFile:
            logFile.write(message["id"] + "\n")
            logFile.close()

    def isNewMessage(self, message: dict):
        with open(self.logFileName, "r") as logFile:
            return (message["id"] not in logFile.read())


    def processMessages(self, messages: list):

        for message in messages:
            self.messageHandler(message)


    def messageHandler(self, message:dict):
        if message["message"].startswith("$echo"):
            contents = message["message"][5:].strip()
            self.zoom.sendMessage(message["channel_id"], contents)



    ### multithreading stuff ###

    def interrupt(self):
        global backgroundThread
        backgroundThread.cancel()


    def backgroundLoop(self):
        global commonData
        global dataLock
        global backgroundThread

        with dataLock:
            messages = self.getMessages()

            print(messages)
            self.processMessages(messages)

        backgroundThread = threading.Timer(self.waitTime, self.backgroundLoop, ())
        backgroundThread.start()


    def initBackgroundLoop(self):
        global backgroundThread

        backgroundThread = threading.Timer(self.waitTime, self.backgroundLoop, ())
        backgroundThread.start()





@app.route("/", methods = ["GET"])
def webhook_read():
    global zoomBot

    if (request.args.get("code") != None):
        zoomBot.zoom.authenticate(request)

    else:
        try:
            print(json.loads(request.data))
        except:
            print(request)

    print("get was called")

    return "200"



@app.route('/', methods=["POST"])
def webhook_action():
    print("POST")
    data = json.loads(request.data)
    print(data)

    return "200"



def main():
    app.run(port = 5000)



if __name__ == '__main__':

    zoomBot = ZoomBot()
    main()
