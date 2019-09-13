import requests
import json
import time
import datetime

YESTERDAY = datetime.date.today() - datetime.timedelta(1)
TODAY = datetime.date.today()
DAY1 = datetime.date.today() + datetime.timedelta(1)
DAY2 = datetime.date.today() + datetime.timedelta(2)
DAY3 = datetime.date.today() + datetime.timedelta(3)
DAY4 = datetime.date.today() + datetime.timedelta(4)
DAY5 = datetime.date.today() + datetime.timedelta(5)
DAY6 = datetime.date.today() + datetime.timedelta(6)
DAY7 = datetime.date.today() + datetime.timedelta(7)


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
	print(gameID)
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

def getBasicGameInfo(gameID):
	response = requests.get("https://statsapi.web.nhl.com/api/v1/game/%s/feed/live" % gameID)
	#print(gameID)
	data = response.json()

	teamAwayAbrv = data["gameData"]["teams"]["away"]["abbreviation"]
	teamHomeAbrv = data["gameData"]["teams"]["home"]["abbreviation"]

	print("%s  %s | " % (teamAwayAbrv, teamHomeAbrv))

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
	tom = getGamesToday(DAY1)
	print("Yesterday (%s)" % YESTERDAY)
	for games in yes:
		#print(games)
		getLiveGameInfo(games)
	print("\nToday (%s)" % TODAY)
	for games in tod:
		#print(games)
		getLiveGameInfo(games)
	print("\nTomorrow (%s)" % DAY1)
	for games in tom:
		#print(games)
		getLiveGameInfo(games)

def getNextWeekGames():
	day1 = getGamesToday(DAY1)
	day2 = getGamesToday(DAY2)
	day3 = getGamesToday(DAY3)
	day4 = getGamesToday(DAY4)
	day5 = getGamesToday(DAY5)
	day6 = getGamesToday(DAY6)
	day7 = getGamesToday(DAY7)
	print("(%s)" % DAY1)
	for games in day1:
		#print(games)
		getBasicGameInfo(games)
	# print("\nToday (%s)" % TODAY)
	print("(%s)" % DAY2)
	for games in day2:
		#print(games)
		getBasicGameInfo(games)
	# print("\nTomorrow (%s)" % DAY1)
	print("(%s)" % DAY3)
	for games in day3:
		#print(games)
		getBasicGameInfo(games)
	print("(%s)" % DAY4)
	for games in day4:
		#print(games)
		getBasicGameInfo(games)
	print("(%s)" % DAY5)
	for games in day5:
		#print(games)
		getBasicGameInfo(games)
	print("(%s)" % DAY6)
	for games in day6:
		#print(games)
		getBasicGameInfo(games)
	print("(%s)" % DAY7)
	for games in day7:
		#print(games)
		getBasicGameInfo(games)

# Test
#glist1 = getGamesToday(YESTERDAY)
#glist2 = getGamesToday(TODAY)
#glist3 = getGamesToday(TOMORROW)

#list = glist1 + glist2 + glist3
#getGameScoresToday(list)

# get3DayGames()
getNextWeekGames()
