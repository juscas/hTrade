import requests
import json
import datetime

def getCurrentTeamIDs():

	response = requests.get("https://statsapi.web.nhl.com/api/v1/teams/")
	data = response.json()

	if (response.status_code != 404):
		print("GET Request successful (%s)" % response.status_code)
	else:
		print("GET Request ERROR (%s)" % response.status_code)
		return

	idList = []

	for team in data['teams']:
		idList.append(team["id"])

	return idList

def activeRosterPlayerIDstoJSON(idList, file):

	f = open(file, 'w')

	f.write("{\n\t\"Updated\": {\n\"date\": \"%s\"\n },\n\n    \"Players\": [ \n" % datetime.datetime.now())

	counter = 0

	for id in idList:

		response = requests.get("https://statsapi.web.nhl.com/api/v1/teams/%s/?expand=team.roster" % id)
		data = json.loads(response.text)

		for player in data['teams'][0]["roster"]["roster"]:
			if counter!=0:
				f.write(",\n")
			else:
				counter +=1
			json.dump(player["person"], f, indent=4)

	f.write("\n]\n}")
	f.close()

def activePlayerIDsToJSON(idList, file):

	f = open(file, 'w')

	f.write("{\n\t\"Updated\": {\n\"date\": \"%s\"\n },\n\n    \"Players\": [ \n" % datetime.datetime.now())

	counter = 0

	for id in idList:

		response = requests.get("https://statsapi.web.nhl.com/api/v1/teams/%s/?expand=team.roster" % id)
		data = json.loads(response.text)

		for player in data['teams'][0]["roster"]["roster"]:
			if counter!=0:
				f.write(",\n")
			else:
				counter +=1
			json.dump(player["person"], f, indent=4)

	f.write("\n]\n}")
	f.close()

ids = getCurrentTeamIDs()

file = generatePlayerIDJSON(ids, "playerlist.json")
