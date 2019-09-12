import requests
import json
import time
import os
from shutil import copyfile

PLAYERSTATSTYPELIST = ["timeOnIce", "assists", "goals", "pim", "shots", "games", "hits", "powerPlayGoals", "powerPlayPoints", "powerPlayTimeOnIce", "evenTimeOnIce", "penaltyMinutes", "faceOffPct", "shotPct", "gameWinningGoals", "overTimeGoals", "shortHandedGoals", "shortHandedPoints", "shortHandedTimeOnIce", "blocked", "plusMinus", "points", "shifts", "timeOnIcePerGame", "evenTimeOnIcePerGame", "powerPlayTimeOnIcePerGame"]
GOALIESTATSTYPELIST = ['timeOnIce', 'ot', 'shutouts', 'ties', 'wins', 'losses', 'saves', 'powerPlaySaves', 'shortHandedSaves', 'evenSaves', 'shortHandedShots', 'evenShots', 'powerPlayShots', 'savePercentage', 'goalAgainstAverage', 'games', 'gamesStarted', 'shotsAgainst', 'goalsAgainst', 'timeOnIcePerGame', 'powerPlaySavePercentage', 'shortHandedSavePercentage','evenStrengthSavePercentage']

PLAYERSFILE = "playerlist.json"

playerNumber = 2

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

	if len(results) == 1:
		print("Found 1 result... %s" % results[0][0])
		writePlayerNameToFile(results[0][0])
		return results[0][1]

	elif len(results) == 0:
		# exception?
		print("%s returned no results." % str1)
		return -1
	else:
		return chooseFromList(results)

def enterPlayerName():
	playerNumber = input("Enter player position (1-3 from right to left)")
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
	writePlayerNameToFile(resultsList[int(choice)-1][0])
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
	results.append(['playerID', playerID])

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
# "timeOnIcePerGame", "evenTimeOnIcePerGame", "powerPlayTimeOnIcePerGame", 'playerID']
#GOALIESTATSTYPELIST = ['timeOnIce', 'ot', 'shutouts', 'ties', 'wins', 'losses', '6saves', 'powerPlaySaves', 'shortHandedSaves',
#  'evenSaves', 'shortHandedShots', 'evenShots', 'powerPlayShots', 'savePercentage', '15goalAgainstAverage', 'games', 
# 'gamesStarted', 'shotsAgainst', 'goalsAgainst', 'timeOnIcePerGame', 'powerPlaySavePercentage', 'shortHandedSavePercentage',
# 'evenStrengthSavePercentage', 'playerID']

def formatStatsString(statsList):
	
	playerSymbolList = ["GP", "G", "A", "P", "PPG", "GWG"]
	goalieSymbolList = ["GP", "W", "Sv%", "GAA", "SO"]

	# if current is a player
	if len(statsList) == 27:
		#statsStr = "GP   {}\nG   {}\nA   {}\nP   {}\nPPG   {}\nGWG   {}\nS%   {}\nTOI/GP   {}\n".format(statsList[5][1], statsList[2][1], statsList[1][1], statsList[21][1], statsList[7][1], statsList[14][1], statsList[13][1], statsList[23][1])
		statsStr = "{:<6} {:<6} {:<7} {:<6} {:<6}\n{:<6} {:<6} {:<6} {:<6} {:<6}".format(playerSymbolList[0], playerSymbolList[1], playerSymbolList[2], playerSymbolList[3], playerSymbolList[4], statsList[5][1], statsList[2][1], statsList[1][1], statsList[21][1], statsList[7][1])
	
	# if current is a goalie
	elif len(statsList) == 24:
 		statsStr = "{:<6} {:<6} {:<6} {:<6} {:<6}\n{:<6} {:<6} {:<6} {:<6} {:<6}".format(goalieSymbolList[0], goalieSymbolList[1], goalieSymbolList[2], goalieSymbolList[3], goalieSymbolList[4], statsList[15][1], statsList[4][1], statsList[13][1], statsList[14][1], statsList[2][1])

	return statsStr

def sendToOBSFolder(statsList):

	id = len(statsList) - 1
	
	# initialize relative file paths
	cwd = os.getcwd()
	picDestDir = cwd + "/OBSPointers/Player/player%s_pic.png" % playerNumber
	statDestDir = cwd + "/OBSPointers/Player/player%s_stats.txt" % playerNumber

	# delete old picture in folder
	os.remove(picDestDir)

	# copy picture from assets folder to OBS pointers folder to send to OBS
	assetSrcDir = cwd[:-7] + "assets/player-pictures/%s.png" % statsList[id][1]
	copyfile(assetSrcDir,picDestDir)

	# write stats string to stats text file to send to OBS
	statsString = formatStatsString(statsList)
	f = open(statDestDir, "w")
	f.write(statsString)
	f.close()

def writePlayerNameToFile(name):
	
	# initialize relative file paths
	cwd = os.getcwd()
	nameDestDir = cwd + "/OBSPointers/Player/player%s_name.txt" % playerNumber

	# write name string to text file to send to OBS
	f = open(nameDestDir, "w")
	f.write(name)
	f.close()

# run player generating script
sendToOBSFolder(getCurrentSeasonPlayerStats(findPlayerId(enterPlayerName(), "playerlist.json")))
#sendToOBSFolder(getCurrentSeasonPlayerStats(findPlayerId(enterPlayerName(), "playerlist.json", 2)), 2)
#sendToOBSFolder(getCurrentSeasonPlayerStats(findPlayerId(enterPlayerName(), "playerlist.json", 3)), 3)
