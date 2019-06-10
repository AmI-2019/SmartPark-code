"""
Provides a list of suggestions for any new incoming car, based on suggestions and availability

Indirectly handles the event 'EntranceArrival'
    - Retrieves user preferences via the API exposed by the UMS (User-Management Server)
    - Retrieves info on the situation inside via the 'spots' module
    - Combines them into a 'UserPrompt' object, ready to be displayed on the touch-screen
    - Maintains a plate -> targetSpot mapping, to answer queries from ACS
"""

import requests
import spots
from typing import List, Dict


DBG: bool
debugPrefix = "ARRIVAL: "
# The next prompt to be displayed on the touch-screen, updated by handleEntranceArrival()
nextPrompt = None
# The last plate number arrived, updated by handleEntranceArrival()
lastPlate: str = ""
# The plate -> targetSpot mapping, written by addChoice() and destructively read by area.target()
targetSpot: Dict[str, int] = {}
# The port for the REST interface exposed by the UMS to the TDS
UM_TDport: int
UM_TD_APIprefix = "/api/v1/"


"""
Encapsulates the information returned by the API
"""
class User:
    def __init__(self, username, preference: int):
        self.username = username
        self.preference = preference


"""
Encapsulates the information to be displayed on the touch-screen
"""
class UserPrompt:
    def __init__(self, username: str, nSpots: int, freeSpots: List[spots.Spot],
                 circulating: int, suggestions: List[spots.Spot]):
        self.username = username
        self.nSpots = nSpots
        self.freeSpots = freeSpots
        self.circulating = circulating
        self.suggestions = suggestions


"""
Retrieves the user information for the supplied plate, via the REST API exposed by the UMS
"""
def getUserFromPlate(plate: str):
    if DBG:
        print(debugPrefix, "getUserFromPlate")
        print("Going to retrieve user from plate ", plate)
        print("")

    resp = requests.get("http://localhost:" + str(UM_TDport) + UM_TD_APIprefix + plate)

    # JSON is decoded into a list
    asList = resp.json()
    if asList == -1:
        asList = ["Person", -1]

    if DBG:
        print("User (asList) = ", asList)
        print(debugPrefix, "getUserFromPlate ENDING")
        print("")

    return User(username=asList[0], preference=int(asList[1]))


"""
Does the actual reasoning, coming up with the list of candidate spots to suggest

Simply filters free spots according to whether their properties include the user preference
"""
def getPromptFromUser(user: User):
    if DBG:
        print(debugPrefix, "getPromptFromUser")
        print("Going to compute list of suggestions for user ", user.username)
        print("")

    if spots.isTransparent():
        if DBG:
            print("Transparency: returning None ")
            print("")
        return None

    freeSpots = spots.getFreeSpots()
    circulating = spots.getCirculating()
    suggestions = []

    for spot in freeSpots:
        if user.preference in spot.properties:
            suggestions.append(spot)

    if DBG:
        print("Returning suggested spots ", [s.ID for s in suggestions])
        print(debugPrefix, "getPromptFromUser ENDING")
        print("")

    return UserPrompt(user.username, spots.nSpots, freeSpots, circulating, suggestions)


"""
Called by 'listener.handleEntranceArrival()'

Makes the 'nextPrompt' ready to be displayed
"""
def handleEntranceArrival(plate: str):
    global nextPrompt, lastPlate

    if DBG:
        print(debugPrefix, "handleEntranceArrival")
        print("Plate ", plate, "arrived at the entrance, going to retrieve user preference")
        print("")

    user = getUserFromPlate(plate)
    lastPlate = plate

    if DBG:
        print("Going to compute prompt")
        print("")

    nextPrompt = getPromptFromUser(user)

    if DBG:
        print(debugPrefix, "handleEntranceArrival ENDING")
        print("")


"""
Called by 'choice.accept()'

Registers user choice for 'lastPlate', the only pending car
"""
def addChoice(spotID: int):
    targetSpot[lastPlate] = spotID

    if DBG:
        print(debugPrefix, "addChoice")
        print("Plate ", lastPlate, ", the only pending car, chose the spot number ", spotID)
        print(debugPrefix, "addChoice ENDING")
        print("")


