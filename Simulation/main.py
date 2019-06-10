"""
The main module, managing MQTT and user interaction.

Connects to a MQTT broker to send plate numbers to.
Launches an interactive menu, asking what simulation to start
"""


import paho.mqtt.client as mqtt
import simulations


DBG: bool = True
debugPrefix = "MAIN: "

clientID = "Simulation"
client: mqtt.Client
brokerHost = "localhost"


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
        sim = input("What simulation (arrival/occupation/exit)?\n")
        if sim == "arrival":
            simulations.arrival()
        elif sim == "occupation":
            simulations.occupation()
        elif sim == "exit":
            simulations.getout()
        else:
            print("Wrong input")




"""
The main function

Sets up the MQTT connection, then launches the menu
"""
if __name__ == '__main__':
    MQTTsetup()
    simulations.init(client)
    menu()

