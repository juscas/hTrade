import requests
import json
import time
import datetime

# TODO
def getTeamId():
	
	response = requests.get("https://statsapi.web.nhl.com/api/v1/teams/")

	if (response.status_code != 404):
		print("GET Request successful (%s)" % response.status_code)
	else:
		print("GET Request ERROR (%s)" % response.status_code)

	data = response.json()
	print(data["teams"][0]["roster"])

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
	#currentTime = data["liveData"]["linescore"]["currentPeriodTimeRemaining"]



	# Game Started, display stats
	if period > 0:
		#print("Period %s\nShots: %s: %s %s: %s" % (period, teamAway, shotsAway, teamHome, shotsHome ))
		#print("Period %s" % period)
		print("Period %s %s %s %s %s" % (period, teamAwayAbrv, goalsAway, teamHomeAbrv, goalsHome))
	else:
		print("Game not yet started.")

	# WAT
def getCurrentTime(gameID):
	currentTime = data["liveData"]["linescore"]["currentPeriodTimeRemaining"]


	# returns list of game IDs from the current date (nhl api refreshes at 12:00 EST)
def getGamesToday():

	response = requests.get("https://statsapi.web.nhl.com/api/v1/schedule")

	data = response.json()

	gamesAmt = data["totalItems"]

	print(gamesAmt)

	gamesList = []

	for i in range(0, gamesAmt):
		gamesList.append(data["dates"][0]["games"][i]["gamePk"])

	return gamesList

def getGameScoresToday(gamesList):
	for games in gamesList:
		getLiveGameInfo(games)

# Test

print(datetime.date.today())

glist = getGamesToday()
getGameScoresToday(glist)

