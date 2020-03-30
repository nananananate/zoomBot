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
        self.zoom = ZoomWrapper()
        self.initBackgroundLoop()
        atexit.register(self.interrupt)



    # multithreading stuff

    def interrupt(self):
        global backgroundThread
        backgroundThread.cancel()


    def backgroundLoop(self):
        global commonData
        global dataLock
        global backgroundThread

        with dataLock:
            print("test")

        backgroundThread = threading.Timer(self.waitTime, self.backgroundLoop, ())
        backgroundThread.start()


    def initBackgroundLoop(self):
        global backgroundThread
        print("starting loop")
        backgroundThread = threading.Timer(self.waitTime, self.backgroundLoop, ())
        backgroundThread.start()












@app.route("/", methods = ["GET"])
def webhook_read():
    global zoomBot


    if (request.args.get("code") != None):

        zoomBot.zoom.authenticate(request)
        # zoomBot.getUsers()
        #zoomBot.getMessages("292922e53c6e4e328e79d2fc9a918653")


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
    print("started")
    app.run(port = 5000)



def backgroundLoop():
    global zoomBot
    count = 0
    while count < 2:
        try:
            time.sleep(5)
        except:
            print("failed")

        count += 1








if __name__ == '__main__':

    zoomBot = ZoomBot()
    #thread = threading.Thread(target = backgroundLoop)
    #thread.start()
    main()
