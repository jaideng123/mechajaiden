import cfg
import re
import requests
commands = {
    '!hello': lambda sock,msg,user: hello(sock,msg,user),
    '!add': lambda sock,msg,user: add(sock,msg,user),
    '!list': lambda sock,msg,user: list(sock,msg,user),
    '!queue': lambda sock,msg,user: queue(sock,msg,user),

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