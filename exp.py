import requests
import json
from collections import defaultdict
from threading import Lock

lock = Lock()
users = defaultdict(int) # Key=username value=EXP
def init():
    print("Initializing EXP")

# Gives a user some amount of experience points
# This should be the only interface used to add points to avoid race conditions
def addExp(user,amount):
    if user == 'all':
        for viewer in listViewers():
            addExp(viewer, amount)
    else:
        with lock:
            users[user] += amount

# Gets a list of current viewers from the Twitch API
def listViewers():
    request_string = 'https://tmi.twitch.tv/group/user/jaideng123/chatters'
    r = requests.get(request_string)
    if(r.status_code == 200):
        res = json.loads(r.text)
        viewers = res['chatters']['viewers'] + res['chatters']['moderators']
    else:
        print('!!! error getting users !!!')
        viewers = []
    return viewers

# write the exp data to a json file
def writeExpData(filepath):
    print('--- SAVING DO NOT CUT ---')
    with open(filepath, 'w') as f:
        f.write(json.dumps(users))
    with open('BACKUP_'+filepath, 'w') as f:
        f.write(json.dumps(users))
    print('--- DONE SAVING ---')
# write the exp data to a json file
def readExpData(filepath):
    with open(filepath, 'r') as f:
        jsonData = f.read()
        newUsers = json.loads(jsonData)
        for user,exp in newUsers.items():
            users[user] = exp
        return
    print('File Does Not Exist')

# calculates the user's level
# I use an arithmetic progression starting from 200, incrementing by 100
def calculateLevel(exp):
    exp_required = 200
    level = 1
    while(exp_required <= exp):
    	level += 1
    	exp_required = exp_required + (exp_required + 20)
    return level,(exp_required-exp)