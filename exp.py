import requests
import json
from collections import defaultdict
from threading import Lock
from math import sqrt
from math import pow

lock = Lock()
users = {} # Key=username value=EXP
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
            if(not (user in users.keys())):
                users[user] = {"activeClass":'fighter'}
                users[user]['exp'] = defaultdict(int)
            activeClass = users[user]['activeClass']
            users[user]['exp'][activeClass] += amount
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
        for user,data in newUsers.items():
            users[user] = {'activeClass':data['activeClass']}
            users[user]['exp'] = defaultdict(int)
            for job,exp in data['exp'].items():
                users[user]['exp'][job] = exp
        return
    print('File Does Not Exist')

# calculates the user's level
# I use a geometric progression scaling by 100
def calculateLevel(exp):
    level = int((sqrt(100*(2*exp + 25))+50)/100)
    exp_required = (pow((level+1),2)+(level+1))/2*100 - ((level+1)*100)
    return level,int(exp_required)-exp
