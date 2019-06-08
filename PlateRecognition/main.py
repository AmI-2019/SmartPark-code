"""
The main module, managing MQTT and user interaction.

Connects to a MQTT broker to send plate numbers to.
Launches an interactive menu, asking when to poll camera and which topic to publish to
"""

import requests
import base64
import json
from functions import cam_init, getpicture
import paho.mqtt.client as mqtt


DBG: bool = True
debugPrefix = "MAIN: "

clientID = "PlateRecognition"
client: mqtt.Client
brokerHost = "localhost"
entranceArrivalTopic = "entrance/plate"
storeyArrivalTopic = "storey/plate"

imagePath = "esempio_1.jpg"
cameraPath = "campic.jpg"
secretKey = "sk_ac131f0dc212d58f2ed6e288"


"""
The callback for when the client receives a CONNACK response from the server.
"""
def on_connect(client, userdata, flags, rc):
    print(debugPrefix, "on_connect")
    print("Connected, result code = ", str(rc))
    print("\n")


"""
Sets up the MQTT connection, starting a separate thread to handle outbound messages
"""
def MQTTsetup():
    global client

    if DBG:
        print(debugPrefix, "MQTTsetup")
        print("Just started; going to connect and start looping")
        print("")

    client = mqtt.Client(client_id=clientID)

    client.on_connect = on_connect

    # Will generate a CONNACK response from the server, triggering the on_connect() callback
    client.connect(brokerHost)

    if DBG:
        print("Connected; going to start looping")
        print("\n")
    # Threaded function that automatically handles reconnection
    client.loop_start()


"""
Continuously asks for a topic, then reads the plate from the camera and publishes it to MQTT
"""
def menu():
    while True:
        while True:
            location = input("Entrance or storey?\n")
            if location == "entrance" or location == "storey":
                break
            print("Wrong input")

        topic = entranceArrivalTopic if location == "entrance" else storeyArrivalTopic
        plate = getPlate()
        if DBG:
            print(debugPrefix, "menu")
            print("Going to publish plate ", plate, " of type ", type(plate), " to the topic ", topic)
            print("")
        client.publish(topic=topic, payload=plate)


"""
Acquires picture from camera, then leverages an open API to convert it to a plate number
"""
def getPlate():
    camera = cam_init()
    pic = getpicture(camera, cameraPath)
    camera.release()

    with open(cameraPath, "rb") as image:
        image_b64 = base64.b64encode(image.read())

    url = "https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=0&country=eu&secret_key=%s" % (secretKey)
    request = requests.post(url, data=image_b64)

    plate_data_str = json.dumps(request.json(), indent=2)
    plate_data_dic = json.loads(plate_data_str)
    plate_number = plate_data_dic["results"][0]["plate"]

    return plate_number


"""
The main function

Sets up the MQTT connection, then launches the menu
"""
if __name__ == '__main__':
    MQTTsetup()
    menu()

