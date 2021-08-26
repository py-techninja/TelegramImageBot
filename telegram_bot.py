import telebot
import os
from telebot import types

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import requests
import json

hostName = "localhost" #should be dynamic incase if  deployed to a server 
serverPort = 8080
API_KEY = 'GET-YOUR-API-KEY-FROM-BOT-FATHER'

def startBot(API_KEY):
    try:
        return telebot.TeleBot(API_KEY)
    except:
        startBot()
    else:
        print("Bot has started")


def sendPhoto(Id, Image):
    bot = startBot(API_KEY)

    return bot.send_photo(chat_id=Id, caption="This is an update from your surveillance", photo=Image)



class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_len = int(self.headers.get('Content-Length'))
        except:
            return
        else:
            post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body.decode("UTF-8"))

        ID = post_body['id']
        Image = open(post_body['image'],'rb') #Image should come in the request as a Buffer object rather then a path name

        try:
            sendPhoto(ID, Image)
        except:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            json_string = json.dumps({'sent': False})
            self.wfile.write(json_string.encode(encoding='utf_8'))
            return
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        json_string = json.dumps({'sent': True})
        self.wfile.write(json_string.encode(encoding='utf_8'))
        return 

        
if __name__ == "__main__":    
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started http:\\\\{hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
