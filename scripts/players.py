import requests
import json
import time

PLAYERSTATSTYPELIST = ["timeOnIce", "assists", "goals", "pim", "shots", "games", "hits", "powerPlayGoals", "powerPlayPoints", "powerPlayTimeOnIce", "evenTimeOnIce", "penaltyMinutes", "faceOffPct", "shotPct", "gameWinningGoals", "overTimeGoals", "shortHandedGoals", "shortHandedPoints", "shortHandedTimeOnIce", "blocked", "plusMinus", "points", "shifts", "timeOnIcePerGame", "evenTimeOnIcePerGame", "powerPlayTimeOnIcePerGame"]
GOALIESTATSTYPELIST = ['timeOnIce', 'ot', 'shutouts', 'ties', 'wins', 'losses', 'saves', 'powerPlaySaves', 'shortHandedSaves', 'evenSaves', 'shortHandedShots', 'evenShots', 'powerPlayShots', 'savePercentage', 'goalAgainstAverage', 'games', 'gamesStarted', 'shotsAgainst', 'goalsAgainst', 'timeOnIcePerGame', 'powerPlaySavePercentage', 'shortHandedSavePercentage','evenStrengthSavePercentage']

PLAYERSFILE = "playerlist.json"

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

def getPlayerStatsByType(playerID, statType="", season=""):

	if statType == "":
		getCurrentSeasonPlayerStats(playerID)

	# exception?
	if playerID == -1:
		# print("No player ID.")
		return -1

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


# TODO: Add a check for goalies and use goalei stattypelist for those
def getCurrentSeasonPlayerStats(playerID):
	if playerID == -1:
		# print("No player ID.")
		return -1

	response = requests.get("https://statsapi.web.nhl.com/api/v1/people/%s/stats/?stats=statsSingleSeason&season=20182019" % (playerID))
	data = response.json()

	if (response.status_code != 404):
		print("GET Request successful (%s)" % response.status_code)
	else:
		print("GET Request ERROR (%s)" % response.status_code)
		return

	stats = data["stats"][0]["splits"][0]["stat"]

	results = []

	if len(stats) == 27:
		for i in range(0, len(PLAYERSTATSTYPELIST)):
			results.append([PLAYERSTATSTYPELIST[i], stats[PLAYERSTATSTYPELIST[i]]])
			# print("%-30s %-4s" % (PLAYERSTATSTYPELIST[i], stats[PLAYERSTATSTYPELIST[i]]))

	elif len(stats) == 23:
 		for i in range(0, len(GOALIESTATSTYPELIST)):
 			results.append([GOALIESTATSTYPELIST[i], stats[GOALIESTATSTYPELIST[i]]])
 			# print("%-30s %-4s" % (GOALIESTATSTYPELIST[i], stats[GOALIESTATSTYPELIST[i]]))

	return results

def compare(pID1, pID2):
	stats1 = getCurrentSeasonPlayerStats(pID1)
	stats2 = getCurrentSeasonPlayerStats(pID2)

	if (len(stats1) != len(stats2)):
		print("Cannot compare two different player types.")
		return 0

	for i in range(len(stats1)):
		print("%-30s %-10s %-4s" % (stats1[i][0], stats1[i][1], stats2[i][1]))


# statType: "yearByYear"
def getCareerNHLStats(playerID):
	return
# PLAYERSTATSTYPELIST = ["timeOnIce", "assists", "goals", "pim", "shots", "games", "hits", "powerPlayGoals", "powerPlayPoints",
#  "powerPlayTimeOnIce", "evenTimeOnIce", "penaltyMinutes", "faceOffPct", "shotPct", "gameWinningGoals", "overTimeGoals", 
# "shortHandedGoals", "shortHandedPoints", "shortHandedTimeOnIce", "blocked", "plusMinus", "points", "shifts", 
# "timeOnIcePerGame", "evenTimeOnIcePerGame", "powerPlayTimeOnIcePerGame"]
#GOALIESTATSTYPELIST = ['timeOnIce', 'ot', 'shutouts', 'ties', 'wins', 'losses', 'saves', 'powerPlaySaves', 'shortHandedSaves',
#  'evenSaves', 'shortHandedShots', 'evenShots', 'powerPlayShots', 'savePercentage', 'goalAgainstAverage', 'games', 
# 'gamesStarted', 'shotsAgainst', 'goalsAgainst', 'timeOnIcePerGame', 'powerPlaySavePercentage', 'shortHandedSavePercentage',
# 'evenStrengthSavePercentage']

def formatStatsString(statsList):
	print(len(statsList))
	# if current is a player
	if len(statsList) == 26:
		statsStr = "Points   {}\n".format(statsList[1][1])
		
	# if current is a goalie
	elif len(statsList) == 22:
 		statsStr = "Points   {}\n".format(statsList[1][1])
	return statsStr

# test

print(formatStatsString(getCurrentSeasonPlayerStats(findPlayerId(enterPlayerName(), "playerlist.json"))))
# getPlayerStatsByType(findPlayerId)
# id1 = findPlayerId(enterPlayerName(), "playerlist.json")
# id2 = findPlayerId(enterPlayerName(), "playerlist.json")
# compare(id1,id2)
# print(getCurrentSeasonPlayerStats(id1))
