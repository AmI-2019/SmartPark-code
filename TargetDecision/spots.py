"""
Keeps track of the current situation inside


Defines a 'Spot' and a 'Storey' class that, together, give a complete overview of the current load status

Indirectly handles some events ('Occupation', 'StoreyArrival', and 'StoreyExit') from the sensors inside:
    - handleOccupation() updates both 'free' and 'circulating'
    - handleStoreyArrival() and handleStoreyExit() only update 'circulating'

Provides useful functions to access information on the situation inside
"""

from typing import List
import arrival


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
    def __init__(self, nSpots, thresh):
        self.nSpots = nSpots
        self.free = nSpots
        self.thresh = thresh
        self.circulating = 0
        self.spots = []
        for i in range(nSpots):
            self.spots.append(Spot(i, []))


DBG: bool
debugPrefix = "SPOTS: "
storey: Storey
nSpots: int


"""
Called by 'listener.handleOccupation()'

Updates 'occupied', 'free', and 'circulating'
"""
def handleOccupation(ID: int, occupied: bool):
    storey.spots[ID].occupied = occupied
    if DBG:
        print(debugPrefix, "handleOccupation")
        print("Affected spot number ", ID, ", occupied = ", occupied)
        print("")

    if occupied:
        storey.free -= 1
        # When a car parks, it no longer is circulating
        storey.circulating -= 1
        if DBG:
            print("Spot number ", ID, " is now occupied, free spots and circulating cars have decreased")
            print("free = ", storey.free, ", circulating = ", storey.circulating)
            print(debugPrefix, "handleOccupation ENDING")
            print("")
    else:
        storey.free += 1
        # When a car exits the spot, it becomes circulating again, until it exits the storey
        storey.circulating += 1
        if DBG:
            print("Spot number ", ID, " is now free, free spots and circulating cars have increased")
            print("free = ", storey.free, ", circulating = ", storey.circulating)
            print(debugPrefix, "handleOccupation, ENDING")
            print("")


"""
Called by 'listener.handleStoreyArrival()'

Updates 'circulating'
"""
def handleStoreyArrival(plate: str):
    storey.circulating += 1
    if DBG:
        print(debugPrefix, "handleStoreyArrival")
        print("Plate ", plate, " just arrived to the storey, circulating cars have increased")
        print("free = ", storey.free, ", circulating = ", storey.circulating)
        print(debugPrefix, "handleStoreyArrival ENDING")
        print("")


"""
Called by 'listener.handleStoreyExit()'

Updates 'circulating'
"""
def handleStoreyExit():
    storey.circulating -= 1
    if DBG:
        print(debugPrefix, "handleStoreyExit")
        print("Someone exited the storey, circulating cars have decreased")
        print("free = ", storey.free, ", circulating = ", storey.circulating)
        print(debugPrefix, "handleStoreyExit ENDING")
        print("")


"""
Returns the number of circulating cars
"""
def getCirculating():
    if DBG:
        print(debugPrefix, "getCirculating")
        print("Returning number of circulating cars")
        print("free = ", storey.free, ", circulating = ", storey.circulating)
        print(debugPrefix, "getCirculating ENDING")
        print("")
    return storey.circulating


"""
Returns the list of free spots
"""
def getFreeSpots():
    freeSpots: List[Spot] = []

    for spot in storey.spots:
        if not spot.occupied and spot.ID not in arrival.targetSpot.values():
            freeSpots.append(spot)

    if DBG:
        print(debugPrefix, "getFreeSpots")
        print("Returning list of free spots")
        print("free = ", storey.free, ", circulating = ", storey.circulating)
        print("freeSpots = ", [s.ID for s in freeSpots])
        print(debugPrefix, "getFreeSpots ENDING")
        print("")

    return freeSpots


def isTransparent():
    res = storey.free - storey.circulating >= storey.thresh
    if DBG:
        print(debugPrefix, "isTransparent")
        print("Deciding whether or not to be transparent")
        print("free = ", storey.free, ", circulating = ", storey.circulating, ", thresh = ", storey.thresh)
        print("Returning ", res)
        print(debugPrefix, "isTransparent ENDING")
        print("")

    return res


"""
Sets the layout and the initial configuration of the storey
"""
def initMap():
    global nSpots, storey

    nSpots = 8
    threshold = 6
    storey = Storey(nSpots, threshold)

    storey.spots[0].properties.append(1)
    storey.spots[1].properties.append(3)
    storey.spots[2].properties.append(3)
    storey.spots[3].properties.append(2)
    storey.spots[4].properties.append(1)
    storey.spots[5].properties.append(3)
    storey.spots[6].properties.append(3)
    storey.spots[7].properties.append(2)

    if DBG:
        print(debugPrefix, "initMap")
        print("Initialising storey layout, nSpots = ", nSpots)
        print("free = ", storey.free, ", circulating = ", storey.circulating)
        print("properties = ", [storey.spots[i].properties for i in range(nSpots)])
        print(debugPrefix, "initMap ENDING")
        print("")
