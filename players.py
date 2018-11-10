import requests
import json
import time


# TODO
def getTeamId():
	
	response = requests.get("https://statsapi.web.nhl.com/api/v1/teams/")

	if (response.status_code != 404):
		print("GET Request successful (%s)" % response.status_code)
	else:
		print("GET Request ERROR (%s)" % response.status_code)

	data = response.json()
	print(data["teams"][0]["roster"])

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
'''
Prints live stats from passed game id
'''
def getLiveGameInfo(gameID):

	response = requests.get("https://statsapi.web.nhl.com/api/v1/game/%s/feed/live" % gameID)

	data = response.json()

	teamAway = data["gameData"]["teams"]["away"]
	teamHome = data["gameData"]["teams"]["home"]

	teamAwayAbrv = data["gameData"]["teams"]["away"]["abbreviation"]
	teamHomeAbrv = data["gameData"]["teams"]["home"]["abbreviation"]

	period = data["liveData"]["linescore"]["currentPeriod"]

	goalsAway = data["liveData"]["linescore"]["teams"]["away"]["goals"]
	goalsHome = data["liveData"]["linescore"]["teams"]["home"]["goals"]

	shotsAway = data["liveData"]["linescore"]["teams"]["away"]["shotsOnGoal"]
	shotsHome = data["liveData"]["linescore"]["teams"]["home"]["shotsOnGoal"]

	# END = 0:00, FINAL = end of game 
	currentTime = data["liveData"]["linescore"]["currentPeriodTimeRemaining"]



	# Game Started, display stats
	if period > 0:
		#print("Period %s\nShots: %s: %s %s: %s" % (period, teamAway, shotsAway, teamHome, shotsHome ))
		print("Period %s %s" % (period, currentTime))
	else:
		print("Game not yet started.")


def getCurrentTime(gameID):
	currentTime = data["liveData"]["linescore"]["currentPeriodTimeRemaining"]


	

def getGamesToday():

	response = requests.get("https://statsapi.web.nhl.com/api/v1/schedule" % gameID)

	data = response.json()





# test 
'''

resultsList = []

id = findPlayerId("brendan gallagher", "playerlist.json", resultsList)

statType = "statsSingleSeason"





print(id)

print(getPlayerStats(id[1], statType))

'''
gameID = 2018020237

while True:
	getLiveGameInfo(gameID)
	time.sleep(1)
