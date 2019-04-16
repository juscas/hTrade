import requests
import json
import time
import datetime

YESTERDAY = datetime.date.today() - datetime.timedelta(1)
TODAY = datetime.date.today()
TOMORROW = datetime.date.today() + datetime.timedelta(1)

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
		if period == 3 and data["liveData"]["linescore"]["currentPeriodTimeRemaining"] == "Final":
			period = 'Final'
		if period == 4 and data["liveData"]["linescore"]["currentPeriodTimeRemaining"] == "Final":
			period = 'Final (OT)'
		if period == 5 and data["liveData"]["linescore"]["currentPeriodTimeRemaining"] == "Final":
			period = 'Final (SO)'

		print("%s %s %s %s | %s" % (teamAwayAbrv, goalsAway, teamHomeAbrv, goalsHome, period))
	else:
		print("%s %s %s %s | %s" % (teamAwayAbrv, "-", teamHomeAbrv, "-", "Not Started"))

	# WAT
def getCurrentTime(gameID):
	currentTime = data["liveData"]["linescore"]["currentPeriodTimeRemaining"]


	# returns list of game IDs from the current date (nhl api refreshes at 12:00 EST)
def getGamesToday(day):

	#dateToday = datetime.date.today()

	response = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?date=%s" % day)

	data = response.json()

	gamesAmt = data["totalItems"]

	# print("%s\n%s games today." % (day, gamesAmt))

	gamesList = []

	for i in range(0, gamesAmt):
		gamesList.append(data["dates"][0]["games"][i]["gamePk"])

	return gamesList

def getGameScoresToday(gamesList):
	for games in gamesList:
		#print(games)
		getLiveGameInfo(games)

def get3DayGames():
	yes = getGamesToday(YESTERDAY)
	tod = getGamesToday(TODAY)
	tom = getGamesToday(TOMORROW)
	print("Yesterday (%s)" % YESTERDAY)
	for games in yes:
		#print(games)
		getLiveGameInfo(games)
	print("\nToday (%s)" % TODAY)
	for games in tod:
		#print(games)
		getLiveGameInfo(games)
	print("\nTomorrow (%s)" % TOMORROW)
	for games in tom:
		#print(games)
		getLiveGameInfo(games)

# Test
#glist1 = getGamesToday(YESTERDAY)
#glist2 = getGamesToday(TODAY)
#glist3 = getGamesToday(TOMORROW)

#list = glist1 + glist2 + glist3
#getGameScoresToday(list)

get3DayGames()
