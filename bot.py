# bot.py

import cfg
import socket
import re
import commands
from time import sleep


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
        pattern = r"!\w+"
        match = re.match(pattern, message)
        if match:
            print(match.group(0))
            commands.commands.get(match.group(0), lambda sock,msg,user: print('command does not exist'))(s,message,username)
                
    sleep(1 / cfg.RATE)