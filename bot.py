# bot.py

import cfg
import commands
import exp
import socket
import re
import requests
import json
from time import sleep
import threading


s = socket.socket()
s.connect((cfg.HOST, cfg.PORT))
s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))

def actionEventLoop():
    CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            line = response
            username = re.search(r"\w+", line).group(0) # return the entire match
            message = CHAT_MSG.sub("", line)
            print(username + ": " + message)
            pattern = r"!\w+"
            match = re.match(pattern, message)
            if match:
                print(match.group(0))
                commands.commands.get(match.group(0), lambda sock,msg,user: print('command does not exist'))(s,message,username)
                sleep(1 / cfg.RATE)

# Hands out exp every EXPINTERVAL seconds
def expEventLoop():
    exp.readExpData('users.json')
    while True:
        exp.addExp('all', 50)
        sleep(cfg.EXPINTERVAL)

#writes exp values every 30 seconds
def expSaveEventLoop():
    while True:
        exp.writeExpData('users.json')
        sleep(30)

def followerEventLoop():
    request_url = 'https://api.twitch.tv/kraken/channels/jaideng123/follows/?limit=1'
    r = requests.get(request_url)
    if(r.status_code == 200):
        res = json.loads(r.text)
        follower = res['follows'][0]['user']['name']
    while True:
        r = requests.get(request_url)
        if(r.status_code == 200):
            res = json.loads(r.text)
            new_follower = res['follows'][0]['user']['name']
            if(new_follower != follower):
                exp.addExp(new_follower,200)
                commands.chat(s,'{} Thanks for the follow, you have recieved 200 EXP'.format(new_follower))
                print('Sent {} initial follow EXP'.format(new_follower))
            follower = new_follower
        else:
            print('!!! error getting follows !!!')
            viewers = []
        sleep(30)

try:
   action_thread = threading.Thread(group=None, target=actionEventLoop, name='Actions-Thread', args=(), kwargs={})
   action_thread.start()
except:
   print("Error: unable to start thread")
try:
   exp_thread = threading.Thread(group=None, target=expEventLoop, name='Exp-Thread', args=(), kwargs={})
   exp_thread.start()
except:
   print("Error: unable to start thread")
try:
   expsave_thread = threading.Thread(group=None, target=expSaveEventLoop, name='Exp-Save-Thread', args=(), kwargs={})
   expsave_thread.start()
except:
   print("Error: unable to start thread")
try:
   follower_thread = threading.Thread(group=None, target=followerEventLoop, name='Follower-Thread', args=(), kwargs={})
   follower_thread.start()
except:
   print("Error: unable to start thread")
