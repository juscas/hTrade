import requests
import json 
import os
import sys
from shutil import copyfile


def getRosterStats(gameID):
	response = requests.get("https://statsapi.web.nhl.com/api/v1/game/%s/feed/live" % (gameID))
	data = response.json()

	if (response.status_code != 404):
		print("GET Request successful (%s)" % response.status_code)
	else:
		print("GET Request ERROR (%s)" % response.status_code)
		return

	#skaters
	roster = data["liveData"]["boxscore"]["teams"]["away"]["skaters"]

	stats = []

	for i in range(0, len(roster)):
		# stats
		try:
			# id, name, position, stats (dict)
			stats.append([roster[i], data["liveData"]["boxscore"]["teams"]["away"]["players"]["ID%s" % roster[i]]["person"]["fullName"], data["gameData"]["players"]["ID%s" % roster[i]]["primaryPosition"]["type"], data["liveData"]["boxscore"]["teams"]["away"]["players"]["ID%s" % roster[i]]["stats"]["skaterStats"]])
		except:
			print("Error! %s doesn't have stats for this game" % data["liveData"]["boxscore"]["teams"]["away"]["players"]["ID%s" % roster[i]]["person"]["fullName"])
		# print(stats[i][1])

	
	return stats

def formatStatsString(statsList):
	
	playerSymbolList = ["GP", "G", "A", "P", "PPG", "GWG"]
	goalieSymbolList = ["GP", "W", "Sv%", "GAA", "SO"]

	# if current is a player
	if len(statsList) == 27:
		statsStr = "{:<6} {:<6} {:<6} {:<6} {:<6}\n{:<6} {:<6} {:<6} {:<6} {:<6}".format(playerSymbolList[0], playerSymbolList[1], playerSymbolList[2], playerSymbolList[3], playerSymbolList[4], statsList[5][1], statsList[2][1], statsList[1][1], statsList[21][1], statsList[7][1])
	
	# if current is a goalie
	elif len(statsList) == 24:
 		statsStr = "{:<6} {:<6} {:<6} {:<6} {:<6}\n{:<6} {:<6} {:<6} {:<6} {:<6}".format(goalieSymbolList[0], goalieSymbolList[1], goalieSymbolList[2], goalieSymbolList[3], goalieSymbolList[4], statsList[15][1], statsList[4][1], statsList[13][1], statsList[14][1], statsList[2][1])

	return statsStr

def sendToOBSFolder(statsList):

	fwdCount = 0
	defCount = 0
	
	for i in range(0, len(statsList)):
		# initialize relative file paths
		cwd = os.getcwd()

		if statsList[i][2] == 'Forward':
			fwdCount += 1
			picDestDir = cwd + "/OBSPointers/Roster/%s%s_pic.png" % (statsList[i][2], fwdCount)
			statDestDir = cwd + "/OBSPointers/Roster/%s%s_stats.txt" % (statsList[i][2], fwdCount)
		else: 
			defCount += 1
			picDestDir = cwd + "/OBSPointers/Roster/%s%s_pic.png" % (statsList[i][2], defCount)
			statDestDir = cwd + "/OBSPointers/Roster/%s%s_stats.txt" % (statsList[i][2], defCount)

		# delete old picture in folder
		try:
			os.remove(picDestDir)
		except:
			print("No file to delete")

		# copy picture from assets folder to OBS pointers folder to send to OBS
		try:
			assetSrcDir = cwd[:-7] + "assets/player-pictures/%s.png" % statsList[i][0]
			copyfile(assetSrcDir,picDestDir)
		except:
			print("fuck, no picture")

		# write stats string to stats text file to send to OBS
		statsString = str(statsList[i][3])
		#formatStatsString(statsList)
		f = open(statDestDir, "w")
		f.write(statsString)
		f.close()

sendToOBSFolder(getRosterStats(2019010047))

# print(getRosterStats(2018020001))