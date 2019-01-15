import re, requests
from bs4 import BeautifulSoup



def getPlayerESPNIDs(pageNo = ""):

    data = requests.get("http://www.espn.com/nhl/statistics/player/_/stat/points/sort/points%s" % pageNo)

    soup = BeautifulSoup(data.text, 'html.parser')

    for table in soup.find_all('table', { 'class': 'tablehead' }):
        values = [a['href'] for a in table.find_all('a', {'href': re.compile(r'id')})]

    print(len(values))
    print(values)




getPlayerESPNIDs()
