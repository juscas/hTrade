import os
import sys
import players
import games
from shutil import copyfile
import datetime

TODAY = datetime.date.today()

tickerStr = ""

# Print top 20 players to ticker text file
#tickerStr += players.getTop20Players(players.sortPlayersByPoints())

# Print Tonight's games to ticker text file
tickerStr += games.getGameScores(games.getGames(TODAY))
# Print News? (( (( 

def writeStringToFile(tickerStr):
	
	# initialize relative file paths
	cwd = os.getcwd()
	tickerDir = cwd + "/OBSPointers/Ticker/ticker.txt"

	# write name string to text file to send to OBS
	f = open(tickerDir, "w")
	f.write(tickerStr)
	f.close()

writeStringToFile(tickerStr)