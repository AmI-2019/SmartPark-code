"""
Keeps track of the current situation inside
"""

class Spot:
    def __init__(self, ID, properties, occupied=False):
        self.ID = ID
        self.properties = properties
        self.occupied = occupied


class Storey:
    def __init__(self, nSpots):
        self.nSpots = nSpots
        self.free = nSpots
        self.circulating = 0
        self.spots = []
        for i in range(nSpots):
            self.spots.append(Spot(i, []))


def handleOccupation(ID: int, occupied: bool):
    storey.spots[ID].occupied = occupied
    if occupied:
        storey.free -= 1
        storey.circulating -= 1
    else:
        storey.free += 1
        storey.circulating += 1


def handleStoreyArrival(plate: str):
    storey.circulating += 1


def handleStoreyExit():
    storey.circulating -= 1


nSpots = 15
storey = Storey(nSpots)