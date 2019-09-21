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
			stats.append([roster[i], data["liveData"]["boxscore"]["teams"]["away"]["players"]["ID%s" % roster[i]]["person"]["fullName"], data["gameData"]["players"]["ID%s" % 8477503]["primaryPosition"]["type"], data["liveData"]["boxscore"]["teams"]["away"]["players"]["ID%s" % roster[i]]["stats"]["skaterStats"]])
		except:
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nErrors:\n%s doesn't have stats for this game\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" % data["liveData"]["boxscore"]["teams"]["away"]["players"]["ID%s" % roster[i]]["person"]["fullName"])

	print(stats[2][3]["timeOnIce"])

def sendToOBSFolder(statsList):

	id = len(statsList) - 1
	
	# initialize relative file paths
	cwd = os.getcwd()
	picDestDir = cwd + "/OBSPointers/Player/player%s_pic.png" % sys.argv[1]
	statDestDir = cwd + "/OBSPointers/Player/player%s_stats.txt" % sys.argv[1]

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


getRosterStats(2018020001)