import requests
import json
import time
import os
import sys
from shutil import copyfile

STATSTYPELIST = ["gamesPlayed", "wins", "losses", "ot", "pts", "ptPctg", "goalsPerGame", "goalsAgainstPerGame", "evGGARatio", "powerPlayPercentage", "powerPlayGoals", "powerPlayGoalsAgainst", "powerPlayOpportunities", "penaltyKillPercentage", "shotsPerGame", "shotsAllowed", "winScoreFirst", "winOppScoreFirst", "winLeadFirstPer", "winLeadSecondPer", "winOutshootOpp", "winOutshotByOpp", "faceOffsTaken", "faceOffsWon", "faceOffsLost", "faceOffWinPercentage", "shootingPctg", "savePctg"]
TEAMLIST = [["NJ", 1], ["NYI", 2], ["NYR", 3], ["PHI", 4], ["PIT", 5], ["BOS", 6], ["BUF", 7], ["MTL", 8], ["OTT", 9], ["TOR", 10], ["CAR", 12], ["FLA", 13], ["TB", 14], ["WSH", 15], ["CHI", 16], ["DET", 17], ["NSH", 18], ["STL", 19], ["CGY", 20], ["COL", 21], ["EDM", 22], ["VAN", 23], ["ANA", 24], ["DAL", 25], ["LA", 26], ["SJ", 28], ["CBJ", 29], ["MIN", 30], ["WPG", 52], ["ARI", 53], ["VGK", 54]]

# Gets team stats from their team ID for the current season 
def getTeamStats(teamID):
	if teamID == -1:
		# print("No team ID.")
		return -1

	response = requests.get("https://statsapi.web.nhl.com/api/v1/teams/%s/stats" % (teamID))
	data = response.json()

	# Check if HTTP request is succesful
	if (response.status_code != 404):
		print("GET Request successful (%s)" % response.status_code)
	else:
		print("GET Request ERROR (%s)" % response.status_code)
		return

	# Compile raw stats with stat types from NHL Stats API json file
	rawStats = data["stats"][0]["splits"][0]["stat"]
	
	# list of pairs of stat names and their values
	stats = []
    
	# Fill stats list from raw stats 
	for i in range(0, 28):
		stats.append([STATSTYPELIST[i], rawStats[STATSTYPELIST[i]]])
		# print(rawStats[STATSTYPELIST[i]])
	
	stats.append(["id", data["stats"][0]["splits"][0]["team"]["id"]])
	stats.append(["name", data["stats"][0]["splits"][0]["team"]["name"]])
	
	return stats

def formatStatsString(statsList):
	statsStr = "{}\n({}-{}-{})\nGP   {:>7}\nPoints   {:>3}\nGF/GP   {:>5}\nGA/GP   {:>7}\nPP%   {:>7}\nPK%   {:>7}\n".format(statsList[29][1], statsList[1][1], statsList[2][1], statsList[3][1], statsList[0][1], statsList[4][1], statsList[6][1], statsList[7][1], statsList[9][1], statsList[13][1])
	return statsStr

def formatRecordString(statsList):
	statsStr = "({} - {} - {})".format(statsList[1][1], statsList[2][1], statsList[3][1])
	return statsStr

# def formatAdvancedStats():

def sendToOBSFolder(statsList, recordPath = "/OBSPointers/Team/team_stats.txt"):
	
	cwd = os.getcwd()
	picDestDir = cwd + "/OBSPointers/Team/team_pic.png"
	statDestDir = cwd + recordPath

	if statsList[28][1] != 8:
		# delete old picture in folder
		os.remove(picDestDir)

		# copy picture from assets folder to OBS pointers folder to send to OBS
		assetSrcDir = cwd[:-7] + "assets/team-pictures/%s.png" % statsList[28][1]
		copyfile(assetSrcDir,picDestDir)

	# write stats string to stats text file to send to OBS
	statsString = formatRecordString(statsList)
	f = open(statDestDir, "w")
	f.write(statsString)
	f.close()


# to modify opposing team in obs

teamID = 8
for i in range(0, len(TEAMLIST)):
	if TEAMLIST[i][0] == sys.argv[1]:
		teamID = TEAMLIST[i][1]
		break
	
# update opposing team stats
sendToOBSFolder(getTeamStats(teamID))
# update habs stats
sendToOBSFolder(getTeamStats(8), "/OBSPointers/Team/habs_stats.txt")
