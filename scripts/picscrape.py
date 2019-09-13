import re, requests, wget
from bs4 import BeautifulSoup
import players



def getPlayerESPNIDs(player):

    name_not_found = 0

    for i in range(0,20):
        print(i)

        pageNo = i*40+1

        # for player pictures: 0, for goalie pictures 1
        if player == 0:
            if i == 0:
                data = requests.get("http://www.espn.com/nhl/statistics/player/_/stat/points/sort/points")
            else:
                data = requests.get("http://www.espn.com/nhl/statistics/player/_/stat/points/sort/points/count/%s" % pageNo)
        else:
            if i == 0:
                data = requests.get("http://www.espn.com/nhl/statistics/player/_/stat/goaltending/sort/avgGoalsAgainst/qualified/false")
            else:
                data = requests.get("http://www.espn.com/nhl/statistics/player/_/stat/goaltending/sort/avgGoalsAgainst/qualified/false/count/%s" % pageNo)



        soup = BeautifulSoup(data.text, 'html.parser')

        for table in soup.find_all('table', { 'class': 'tablehead' }):
            values = [a['href'] for a in table.find_all('a', {'href': re.compile(r'id')})]

        for value in values:
            id = re.sub("\D", "", value)
            name = value[len(id)+37:]
            name = re.sub("-", " ", name)
            realID = players.findPlayerId(name, "playerlist.json")
            print(name)

            if realID == -1:
                name_not_found += 1
                realID = name

            testUrl = requests.get("http://a.espncdn.com/combiner/i?img=/i/headshots/nhl/players/full/%s.png" % id)

            if testUrl.status_code == 404:
                continue

            url = "http://a.espncdn.com/combiner/i?img=/i/headshots/nhl/players/full/%s.png" % id
            out_filepath = "/home/justin/Pictures/pictest/%s.png" % realID
            filename = wget.download(url, out_filepath)
            #print("%s, %s " % (id, name))
        print("No IDs: %s\n" % name_not_found)


# scrape for player pictures
getPlayerESPNIDs(0)
# scrape for goalie pictures
getPlayerESPNIDs(1)

