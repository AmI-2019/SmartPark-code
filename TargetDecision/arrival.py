import requests
import spots
import threading

nextPrompt = None
promptLock = threading.Lock()
UM_TDport = 5000
UM_TD_APIprefix = "/api/v1/"


class User:
    def __init__(self, username, preference):
        self.username = username
        self.preference = preference


class UserPrompt:
    def __init__(self, free: int, circulating: int, suggestions: list[spots.Spot]):
        self.free = free
        self.circulating = circulating
        self.suggestions = suggestions


def getUserFromPlate(plate: str):
    resp = requests.get(url="localhost:" + str(UM_TDport) + UM_TD_APIprefix + plate)
    asDict = resp.json()

    return User(asDict["username"], asDict["preference"])


def getPromptFromUser(user: User):
    free = spots.getFree()
    circulating = spots.getCirculating()
    suggestions = []

    for spot in spots.getFreeSpots():
        if user.preference in spot.properties:
            suggestions.append(spot)

    return UserPrompt(free, circulating, suggestions)


def handleEntranceArrival(plate: str):
    global nextPrompt
    user = getUserFromPlate(plate)
    nextPrompt = getPromptFromUser(user)
    promptLock.release()


def main():
    promptLock.acquire()