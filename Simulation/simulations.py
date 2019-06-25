import main
import paho.mqtt.client as mqtt


client: mqtt.Client
nSpots = 8
occupationTopic = "storey/spot/"
debugOccupationTopic = "DBG/storey/spot/"
entranceArrivalTopic = "entrance/plate"
storeyArrivalTopic = "storey/plate"
storeyExitTopic = "storey/exit"


def arrival():
    plate = input("Enter plate: ")
    client.publish(entranceArrivalTopic, plate)
    input("Now check the Tablet (enter when you're done)")
    client.publish(storeyArrivalTopic, plate)
    spot = input("Enter spot to go to: ")
    client.publish(occupationTopic + str(spot), str(1))
    print("Done\n\n")


def occupation():
    spot = input("Enter spot to forcefully occupy: ")
    client.publish(debugOccupationTopic + str(spot), str(1))
    print("Done\n\n")


def selective():
    freestr = input("Enter spots (space separated) to be left free: ")
    free = [int(spot) for spot in freestr.split(" ")]

    for spot in range(nSpots):
        if spot in free:
            client.publish(debugOccupationTopic + str(spot), str(0))
        else:
            client.publish(debugOccupationTopic + str(spot), str(1))

    print("Done\n\n")


def getout():
    spot = input("Enter spot to get out of: ")
    client.publish(occupationTopic + str(spot), str(0))
    input("Press enter to exit the car park")
    client.publish(storeyExitTopic, "")
    print("Done\n\n")


def init(cl):
    global client

    client = cl
