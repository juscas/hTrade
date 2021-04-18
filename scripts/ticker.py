import os
import sys
import requests
import json
#import players
import games
from shutil import copyfile
import datetime

TODAY = datetime.date.today()
PLAYERSFILE = "playerlist.json"

def sortPlayersByPoints():
	results = []

	with open(PLAYERSFILE, 'r') as f:
		playerListJSON = json.load(f)

	for player in playerListJSON["Players"]:
		playerName = player["fullName"]
		#print(playerName)
		pointsTuple = getPoints(player["id"])
		results.append([playerName, pointsTuple])
	
	return(sorted(results, key = lambda x: x[1], reverse=True))
	

def getPoints(playerID):
	response = requests.get("https://statsapi.web.nhl.com/api/v1/people/%s/stats/?stats=statsSingleSeason&season=20202021" % (playerID))
	data = response.json()

	if (response.status_code != 404):
		print("GET Request successful (%s)" % response.status_code)
	else:
		print("GET Request ERROR (%s)" % response.status_code)
		return

	try:
		points = data["stats"][0]["splits"][0]["stat"]["points"]
		assists = data["stats"][0]["splits"][0]["stat"]["assists"]
		goals = data["stats"][0]["splits"][0]["stat"]["goals"]
	except:
		points = 0
		assists = 0
		goals = 0
		print("Player is a goalie.")
	return [points, goals, assists]

def getTop20Players(playerList):
	outputStr = ""
	for i in range(20):
		outputStr += "%s. %s:   %s G   %s A   %s P       " % ((i+1), playerList[i][0], playerList[i][1][1], playerList[i][1][2], playerList[i][1][0])
	return outputStr

def writeStringToFile(tickerStr):
	
	# initialize relative file paths
	cwd = os.getcwd()
	tickerDir = cwd + "/OBSPointers/Ticker/ticker.txt"

	# write name string to text file to send to OBS
	f = open(tickerDir, "w")
	f.write(tickerStr)
	f.close()


tickerStr = ""

# Print top 20 players to ticker text file
tickerStr += "|    2020-2021 Top Scorers   "
tickerStr += getTop20Players(sortPlayersByPoints())

# Print Tonight's games to ticker text file
tickerStr += "|    Tonight's Matchups   "
tickerStr += games.getGameScores(games.getGames(TODAY))
# Print News? (( (( 

writeStringToFile(tickerStr)