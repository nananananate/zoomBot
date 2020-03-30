# By Nathaniel Louis Tisuela
from flask import Flask, request
import requests
import json
import base64
import time
import threading




class ZoomWrapper:
    def __init__(self):
        self.credentialsFileName = "credentials.json"
        self.credentials = readJson(self.credentialsFileName)

        self.usersUrl = "https://api.zoom.us/v2/users"
        self.oauthUrl = "https://zoom.us/oauth/token"
        self.messagesUrl = "https://api.zoom.us/v2/chat/users/me/messages"

        self.users = []
        self.me = "rRMd0H_aQ9yf2mGhVEXM5Q"

        self.credentials["redirectUri"] = "http://a86e7e32.ngrok.io"
        self.credentials["clientId"] = "m1uvYOTfSd2ADAO4b5gtuQ"#"vQAVi0P7Q3WXIxE_ib8Aeg"
        self.credentials["clientSecret"] = "UZmsMiBmcw9QxwQs3Djslyg9iIU61tfO"#"FAH3BrDjhPcoq4VXFA5hE2JKYanrgfaM"

        clientId = self.credentials["clientId"]
        clientSecret = self.credentials["clientSecret"]
        encodedString =f"{clientId}:{clientSecret}".encode("ascii")
        self.clientEncoded = base64.b64encode(encodedString).decode("utf-8")



    def authenticate(self, request):
        codeDict = {"code": request.args.get("code")}
        self.credentials.update(codeDict)

        params = {"grant_type": "authorization_code", "code": self.credentials["code"],
                    "redirect_uri": self.credentials["redirectUri"]}
        headers = {"Authorization": "Basic " + self.clientEncoded}

        response = requests.post(self.oauthUrl,
                    params = params, headers = headers)
        self.credentials.update(json.loads(response.text))
        #print(response.text)
        #print(self.credentials)
        self.__saveCredentials()


    def getUsers(self):
        headers = {"Authorization": "Bearer " + self.credentials["access_token"]}
        response = requests.get(self.usersUrl, headers=headers)
        responseDict = json.loads(response.text)
        #print(responseDict)
        self.users = responseDict["users"]


    def getChannels(self):
        url = "https://api.zoom.us/v2/chat/users/me/channels"
        headers = {"Authorization": "Bearer " + self.credentials["access_token"]}
        response = requests.get(url, headers = headers)
        print("got channels")
        print(response.text)

    def getChannel(self, channelId: str):
        channelId = "292922e53c6e4e328e79d2fc9a918653"
        url = f"https://api.zoom.us/v2/chat/channels/{channelId}"
        headers = {"Authorization": "Bearer " + self.credentials["access_token"]}
        response = requests.get(url, headers = headers)
        print("channel")
        print(response.text)


    def sendMessage(self, channelId: str, message: str):
        message = "YEET this is the bot's message"

        headers = {"Authorization": "Bearer " + self.credentials["access_token"],
                    "content-type": "application/json"}

        params = {"to_channel": channelId}
        data = {"message": message, "to_channel": channelId}
        response = requests.post(self.messagesUrl, headers = headers, data= json.dumps(data))

        print(response.text)


    def getChannelMessages(self, channelId: str) -> dict:

        headers = {"Authorization": "Bearer " + self.credentials["access_token"],
                    "content-type": "application/json"}

        params = {"to_channel": channelId}


        response = requests.get(self.messagesUrl, headers = headers, params = params)

        return json.loads(response.text)


    def __saveCredentials(self):
        writeJson(self.credentialsFileName, self.credentials)






def readJson(filename: str) -> dict:
    with open(filename, "r") as file:
        data = json.load(file)
        file.close()
        return data

def writeJson(filename: str, data: dict) -> None:
    with open(filename, "w") as file:
        json.dump(data, file)
        file.close()
