# A tiny script to update current json data to a new format
import exp
from collections import defaultdict
import json

with open('users.json','r') as f:
	jsonData = f.read()
	users = json.loads(jsonData)
newusers = {}

for user,exp in users.items():
	newusers[user] = {'activeClass':"fighter"}
	newusers[user]['exp'] = defaultdict(int)
	newusers[user]['exp']["fighter"] = exp
print('--- SAVING DO NOT CUT ---')
with open("users_NEW", 'w') as f:
	f.write(json.dumps(newusers))
print('--- DONE SAVING ---')
