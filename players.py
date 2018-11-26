import requests
import json
import time

def findPlayerId(str1, jsonPlayersFile, results):
	str1 = str1.lower()

	with open(jsonPlayersFile, 'r') as f:
		playerListJSON = json.load(f)

	print("Searching for \"%s\"..." % str1)
		
	for player in playerListJSON["Players"]:
		fullName = player["fullName"].lower()

		result = fullName.find(str1)

		if result != -1:
			results.append([player["fullName"], player["id"]])
		#else:
			#"String not found.")
	if len(results) == 1:
		return results[0]
	else:
		return results

#TODO - refine
def getPlayerStats(playerID, statType):
	
	response = requests.get("https://statsapi.web.nhl.com/api/v1/people/%s/stats/?stats=%s" % (playerID, statType))
	data = response.json()

	if (response.status_code != 404):
		print("GET Request successful (%s)" % response.status_code)
		return data
	else:
		print("GET Request ERROR (%s)" % response.status_code)
		return

# test 


resultsList = []

id = findPlayerId("brendan gallagher", "playerlist.json", resultsList)

statType = "statsSingleSeason"





print(id)

print(getPlayerStats(id[1], statType))



