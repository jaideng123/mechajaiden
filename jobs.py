import exp
import json

jobs = {}
# Grab the current list of jobs
with open('classes.json', 'r') as f:
        jsonData = f.read()
        jobs = json.loads(jsonData)

def flavorText(job,ability,user,target):
	text = jobs[job]['actions'][ability]['success']
	text = text.replace('<PLAYER>',user)
	text = text.replace('<TARGET>',target)
	return text

def jobList():
	joblist = []
	for name,job in jobs.items():
		joblist.append(name)
	return joblist

def setJob(user,job):
	if(job in jobList()):
		with exp.lock:
			exp.users[user]['activeClass'] = job
		return True
	else:
		return False
def getJob(user):
	return exp.users[user]['activeClass']