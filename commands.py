import cfg
import exp
import re
import requests
import json
from datetime import datetime
from dateutil import parser


commands = {
    '!hello': lambda sock,msg,user: hello(sock,msg,user),
    '!add': lambda sock,msg,user: add(sock,msg,user),
    '!list': lambda sock,msg,user: list(sock,msg,user),
    '!queue': lambda sock,msg,user: queue(sock,msg,user),
    '!level': lambda sock,msg,user: level(sock,msg,user),
    '!giveexp': lambda sock,msg,user: giveexp(sock,msg,user),
    '!uptime': lambda sock,msg,user: uptime(sock,msg,user)

}

#Command Functions

# Says Hello
def hello(sock,msg,user):
    chat(sock,'Greetings '+user+', I am TwitchBot-XJ-9. But you may call me MechaJaiden')

# Adds a mario maker level
def add(sock,msg,user):
    print(msg)
    levelcode = re.search(r"([\dA-Z]{4}-[\dA-Z]{4}-[\dA-Z]{4}-[\dA-Z]{4})+",msg)
    if(levelcode):
        levelcode = levelcode.group(0)
    print(levelcode)
    request_string = 'http://warp.world/bot/add?streamer=jaideng123&submitter={}&key={}&levelcode={}'.format(user, cfg.WARPWORLDKEY,levelcode)
    r = requests.get(request_string)
    if(r.status_code == 200):
        chat(sock,r.text)

# Shows user their submitted levels
def list(sock,msg,user):
    request_string = 'http://warp.world/bot/list?streamer=jaideng123&key={}&submitter={}'.format(cfg.WARPWORLDKEY,user)
    r = requests.get(request_string)
    if(r.status_code == 200):
        chat(sock,r.text)

# Shows user their submitted levels
def queue(sock,msg,user):
    request_string = 'http://warp.world/bot/queue?streamer=jaideng123&key={}&submitter={}'.format(cfg.WARPWORLDKEY, user)
    r = requests.get(request_string)
    if(r.status_code == 200):
        chat(sock,r.text)

#Displays the user's current exp level
def level(sock,msg,user):
    level, diff = exp.calculateLevel(exp.users[user])
    chat(sock,'{} You Are Currently Level {} ({} exp away from level {})'.format(user,level,diff,level+1))

#Tells the user how long the stream has been up
def uptime(sock,msg,user):
    request_string = 'https://api.twitch.tv/kraken/streams/jaideng123'
    r = requests.get(request_string)
    if(r.status_code == 200):
        stream = json.loads(r.text)
        if stream['stream']:
            today = datetime.utcnow().replace(tzinfo=None)
            stream_start = parser.parse(stream['stream']['created_at']).replace(tzinfo=None)
            s = (today-stream_start).seconds
            hours, remainder = divmod(s, 3600)
            minutes, seconds = divmod(remainder, 60)
            chat(sock,'Jaiden has been streaming for {} Hours and {} Minutes'.format(hours,minutes))
        else:
            chat(sock,'Jaiden is currently not online')
    else:
        chat(sock,'Tell Jaiden he needs to fix me')

#Give Exp to a user (or all)
def giveexp(sock,msg,user):
    if(user != 'jaideng123'):
        chat(sock,'Sure I\'ll get right on tha- wait a second, you\'re not Jaiden!')
        return
    recipient = msg.split(' ')[1]
    amount = msg.split(' ')[2].split('\n')[0]
    print(recipient,amount)
    exp.addExp(recipient,int(amount))
    if(recipient == 'all'):
        chat(sock,'Everyone Has Received {} Experience Points'.format(amount))
    else:
        chat(sock,'{} Has Received {} Experience Points'.format(recipient,amount))




# Utility functions

def chat(sock, msg):
    """
    Send a chat message to the server.
    Keyword arguments:
    sock -- the socket over which to send the message
    msg  -- the message to be sent
    """
    sent ="PRIVMSG {} :{}\r\n".format(cfg.CHAN, msg).encode("utf-8") 
    sock.send(sent)

def ban(sock, user):
    """
    Ban a user from the current channel.
    Keyword arguments:
    sock -- the socket over which to send the ban command
    user -- the user to be banned
    """
    chat(sock, ".ban {}".format(user))

def timeout(sock, user, secs=600):
    """
    Time out a user for a set period of time.
    Keyword arguments:
    sock -- the socket over which to send the timeout command
    user -- the user to be timed out
    secs -- the length of the timeout in seconds (default 600)
    """
    chat(sock, ".timeout {}".format(user, secs))