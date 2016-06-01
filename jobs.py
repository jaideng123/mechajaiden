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