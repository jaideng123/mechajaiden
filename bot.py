# bot.py

import cfg
import socket
import re
from time import sleep

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


CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

s = socket.socket()
s.connect((cfg.HOST, cfg.PORT))
s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))

while True:
    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        line = response
        username = re.search(r"\w+", line).group(0) # return the entire match
        message = CHAT_MSG.sub("", line)
        print(username + ": " + message)
        for pattern in cfg.PATT:
            if re.match(pattern, message):
                if(pattern == r"!hello"):
                    chat(s, 'Greetings human, I am TwitchBot-XJ-9. But you may call me MechaJaiden')
                    break
                if(pattern == r"!purpose"):
                    chat(s, 'To learn from my master until i am sufficient enough to replace him')
                    break
    sleep(1 / cfg.RATE)