import exp
import json

jobs = {}
# Grab the current list of jobs
with open('classes.json', 'r') as f:
        jsonData = f.read()
        jobs = json.loads(jsonData)

def flavorText(job,ability,user,target):
	if(not (ability in jobs[job]['actions'].keys())):
		return "This action does not exist for you current job"
	required_level = jobs[job]['actions'][ability]['levelreq']
	user_level,diff = exp.calculateLevel(exp.users[user]['exp'][getJob(user)]) 
	if(user_level >= required_level):
		text = jobs[job]['actions'][ability]['success']
		text = text.replace('<PLAYER>',user)
		text = text.replace('<TARGET>',target)
		return text
	else:
		return "{} You must be a level {} {} to use this ability".format(user,required_level,job)


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