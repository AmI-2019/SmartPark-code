"""
Handles the arrival of a car to the storey.

Asks to the TDS, via REST API, the target spot for the new car.
Commands the Gateway, via MQTT, to light up the right LEDs.
"""

import requests
import listener


DBG: bool
debugPrefix = "ARRIVAL: "

TD_ACport: int
TD_AC_APIprefix = "/target/"

# Dependant on the storey layout
# -1 is received by getTargetFromPlate() when transparent behaviour is required
LEDs = {-1: "", 0: ",0,1", 7: ",0,2,3,4"}
LEDtopic = "/strip/LED"


"""
Makes a request to the TDS, providing a plate and expecting a target spot.
"""
def getTargetFromPlate(plate: str):
    if DBG:
        print(debugPrefix, "getTargetFromPlate")
        print("Requesting target spot for plate ", plate)
        print("")

    resp = requests.get("localhost:" + str(TD_ACport) + TD_AC_APIprefix + plate)
    spotID = int(resp.text)

    if DBG:
        print("Received target spot ", spotID)
        print(debugPrefix, "getTargetFromPlate ENDING")
        print("")

    return spotID


"""
Publishes an MQTT messages to the LEDtopic, specifying the LEDs to be lighted up
"""
def lightLEDs(spotID):
    if DBG:
        print(debugPrefix, "lightLEDs")
        print("Commanding to light up LEDs for spot ", spotID)
        print("")

    payload = str(spotID) + LEDs[spotID]
    listener.client.publish(topic=LEDtopic, payload=payload)
    listener.client.wait_for_publish()

    if DBG:
        print("Successfully published payload ", payload)
        print(debugPrefix, "lightLEDs ENDING")
        print("")


"""
Is called by listener.handleStoreyArrival()

Retrieves target spot and lights up the corresponding LEDs
"""
def handleStoreyArrival(plate: str):
    if DBG:
        print(debugPrefix, "handleStoreyArrival")
        print("Plate ", plate, " just arrived to the storey")
        print("Going to retrieve target spot")
        print("")

    spotID = getTargetFromPlate(plate)

    if DBG:
        print("Going to light up LEDs ")
        print("")

    lightLEDs(spotID)

    if DBG:
        print(debugPrefix, "handleStoreyArrival ENDING")
        print("")

