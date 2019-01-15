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

	resultCount = len(results)

	if len(results) == 1:
		print("Found 1 result... %s" % results[0][0])
		return results[0][1]

	elif len(results) == 0:
		# exception?
		print("%s returned no results." % str1)
		return -1
	else:
		return chooseFromList(results)

def enterPlayerName():
	searchStr = input("Search for a player:")
	return searchStr

def chooseFromList(resultsList):
	counter = 1
	for entry in resultsList:
		print("[%s]%s" % (counter, entry[0]))
		counter += 1

	choice = -1

	while int(choice) > len(resultsList) or int(choice) < 1:
		if choice != -1:
			print("Invalid entry. Input a number corresponding to the desired player.")
		choice = input("Choose a player:")
	print("Displaying results for: \n%s\n" % resultsList[int(choice)-1][0])
	return resultsList[int(choice)-1][1]

def getPlayerStatsByType(playerID, statType, season=""):

	# exception?
	if playerID == -1:
		# print("No player ID.")
		return -1;

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


def getPlayerName(playerID):
	response = requests.get("https://statsapi.web.nhl.com/api/v1/people/%s/" % (playerID))
	data = response.json()
	name = data["people"][0]["fullName"]
	return name


# TODO: Add a check for goalies and use goalie stattypelist
def getCurrentSeasonPlayerStats(playerID):
	if playerID == -1:
		# print("No player ID.")
		return -1;

	response = requests.get("https://statsapi.web.nhl.com/api/v1/people/%s/stats/?stats=statsSingleSeason" % (playerID))
	data = response.json()
	stats = data["stats"][0]["splits"][0]["stat"]

	results = {}
	results["name"] = getPlayerName(playerID)

	for i in range(0, len(playerStatsTypeList)):
		results[playerStatsTypeList[i]] = stats[playerStatsTypeList[i]]
		#print("%-30s %-4s" % (playerStatsTypeList[i], stats[playerStatsTypeList[i]]))

	results_dict = []
	results_dict.append(results.copy())
	return results_dict;


# statType: "yearByYear"
def getCareerNHLStats(playerID):
	return

# test

print(getPlayerName(8480829))

# print(getCurrentSeasonPlayerStats(8480829))

# getCurrentSeasonPlayerStats(findPlayerId(enterPlayerName(), "playerlist.json"))
