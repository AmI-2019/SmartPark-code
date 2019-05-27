"""
Keeps track of the current situation inside


Defines a 'Spot' and a 'Storey' class that, together, give a complete overview of the current load status

Indirectly handles some events ('Occupation', 'StoreyArrival', and 'StoreyExit') from the sensors inside:
    - handleOccupation() updates both 'free' and 'circulating'
    - handleStoreyArrival() and handleStoreyExit() only update 'circulating'

Provides useful functions to access information on the situation inside
"""

from typing import List


"""
ID: storey-unique identifier
properties: list of desirable qualities of the spot that can be selected by the user
occupied: boolean flag
"""
class Spot:
    def __init__(self, ID, properties, occupied=False):
        self.ID = ID
        self.properties = properties
        self.occupied = occupied


"""
nSpots: total number of spots
free: number of free spots, dynamically changes
circulating: number of circulating cars, dynamically changes
spots: list of all spots
"""
class Storey:
    def __init__(self, nSpots):
        self.nSpots = nSpots
        self.free = nSpots
        self.circulating = 0
        self.spots = []
        for i in range(nSpots):
            self.spots.append(Spot(i, []))


storey: Storey
nSpots: int


"""
Called by 'listener.handleOccupation()'

Updates 'occupied', 'free', and 'circulating'
"""
def handleOccupation(ID: int, occupied: bool):
    storey.spots[ID].occupied = occupied
    if occupied:
        storey.free -= 1
        # When a car parks, it no longer is circulating
        storey.circulating -= 1
    else:
        storey.free += 1
        # When a car exits the spot, it becomes circulating again, until it exits the storey
        storey.circulating += 1


"""
Called by 'listener.handleStoreyArrival()'

Updates 'circulating'
"""
def handleStoreyArrival(plate: str):
    storey.circulating += 1


"""
Called by 'listener.handleStoreyExit()'

Updates 'circulating'
"""
def handleStoreyExit():
    storey.circulating -= 1


"""
Returns the number of free spots
"""
def getFree():
    return storey.free


"""
Returns the number of circulating cars
"""
def getCirculating():
    return storey.circulating


"""
Returns the list of free spots
"""
def getFreeSpots():
    freeSpots: List[Spot] = []

    for spot in storey.spots:
        if not spot.occupied:
            freeSpots.append(spot)

    return freeSpots


"""
Sets the layout and the initial configuration of the storey
"""
def initMap():
    global nSpots, storey
    nSpots = 15
    storey = Storey(nSpots)
