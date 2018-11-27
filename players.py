import requests
import json
import time

playerStatsTypeList = ["timeOnIce", "assists", "goals", "pim", "shots", "games", "hits", "powerPlayGoals", "powerPlayPoints", "powerPlayTimeOnIce", "evenTimeOnIce", "penaltyMinutes", "faceOffPct", "shotPct", "gameWinningGoals", "overTimeGoals", "shortHandedGoals", "shortHandedPoints", "shortHandedTimeOnIce", "blocked", "plusMinus", "points", "shifts", "timeOnIcePerGame", "evenTimeOnIcePerGame", "powerPlayTimeOnIcePerGame"]
goalieStatsTypeList = ['timeOnIce', 'ot', 'shutouts', 'ties', 'wins', 'losses', 'saves', 'powerPlaySaves', 'shortHandedSaves', 'evenSaves', 'shortHandedShots', 'evenShots', 'powerPlayShots', 'savePercentage', 'goalAgainstAverage', 'games', 'gamesStarted', 'shotsAgainst', 'goalsAgainst', 'timeOnIcePerGame', 'powerPlaySavePercentage', 'shortHandedSavePercentage','evenStrengthSavePercentage']

def findPlayerId(str1, jsonPlayersFile):
	results = []

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
		return results[0][1]
	else:
		return chooseFromList(results)

def chooseFromList(resultsList):
	counter = 1
	for entry in resultsList:
		print("[%s]%s" % (counter, entry[0]))
		counter += 1

	choice = input("choose:")
	return resultsList[int(choice)-1][1] 	

def getPlayerStatsByType(playerID, statType, season=""):
	
	response = requests.get("https://statsapi.web.nhl.com/api/v1/people/%s/stats/?stats=%s&season=%s" % (playerID, statType, season))
	data = response.json()
	
	if (response.status_code != 404):
		print("GET Request successful (%s)" % response.status_code)
		return data
	else:
		print("GET Request ERROR (%s)" % response.status_code)
		return

	goals = data.keys()
	print(goals)

def getCurrentSeasonPlayerStats(playerID):
	response = requests.get("https://statsapi.web.nhl.com/api/v1/people/%s/stats/?stats=statsSingleSeason" % (playerID))
	data = response.json()
	stats = data["stats"][0]["splits"][0]["stat"]

	results = []

	for i in range(0, len(playerStatsTypeList)):
		results.append([playerStatsTypeList[i], stats[playerStatsTypeList[i]]])
		print("%s: %s" % (playerStatsTypeList[i], stats[playerStatsTypeList[i]]))

	return results;


# statType: "yearByYear"
def getCareerNHLStats(playerID): 
	return

# test 


id = findPlayerId("justin", "playerlist.json")

statType = "statsSingleSeason"




'''
print(id)

print(getPlayerStatsByType(id[1], statType))
'''

print(id)

print(getCurrentSeasonPlayerStats(id))



