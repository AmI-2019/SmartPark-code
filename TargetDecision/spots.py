class Spot:
    def __init__(self, id, properties, occupied=False):
        self.id = id
        self.properties = properties
        self.occupied = occupied


    def setOccupied(self):
        self.occupied = True


    def setFree(self):
        self.occupied = False


class Storey:
    def __init__(self, nSpots):
        self.nSpots = nSpots
        self.spots = []
        for i in range(nSpots):
            self.spots.append(Spot(i, []))

def setSpot(id, occupied):
    storey.spots[id].occupied = occupied


nSpots = 15
storey = Storey(nSpots)