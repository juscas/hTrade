import players

class Player:

    def __init__(self):
        name = "undefined"
        stats = []

    def __init__(self, playerID):
        self.playerID = playerID
        self.stats = players.getCurrentSeasonPlayerStats(playerID)

# test
x = Player(8480965)
print(x.stats)
