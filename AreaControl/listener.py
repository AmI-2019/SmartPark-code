"""
Listens for incoming MQTT messages.


Connects to the remote broker, and masks connection breakdowns:
    - Automatically handles reconnection, through the loop_forever() function
    - Subscriptions are renewed after each reconnection, as they are made after a CONNACK response is received

Dispatches messages to appropriate functions from other modules:
    - Extracts relevant information from topic and payload
    - Passes them to the appropriate function from the other modules, thus adapting to their signature and
      masking to them the underlying MQTT infrastructure
"""

import paho.mqtt.client as mqtt
import arrival


DBG: bool
debugPrefix = "LISTENER: "
client = None
brokerHost = "localhost"
clientID = "AreaControl"
storeyArrivalTopic = "storey/plate"

"""
The callback for when the client receives a CONNACK response from the server.

Subscriptions are made here, so that they are automatically renewed at every reconnection.
"""
def on_connect(client, userdata, flags, rc):
    if DBG:
        print(debugPrefix, "on_connect")
        print("Connected, result code = ", str(rc))
        print("Going to subscribe")
        print("")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(storeyArrivalTopic)

    if DBG:
        print("Subscribed")
        print(debugPrefix, "on_connect ENDING")
        print("")


"""
The callback for when a car approaches the entrance of the storey.

The message is structured as follows:
    Topic = /storey/plate
    Payload = plate number

This event is handled by the 'arrival' module.
"""
def handleStoreyArrival(client, userdata, msg):
    plate = str(msg.payload.decode())
    if DBG:
        print(debugPrefix, "handleStoreyArrival")
        print("Plate = ", plate)
        print("Going to call arrival.handleStoreyArrival")
        print("")

    arrival.handleStoreyArrival(plate)

    if DBG:
        print(debugPrefix, "handleStoreyArrival ENDING")
        print("")


"""
The callback for when a message is received that matches against none of the specific topics
"""
def on_message(client, userdata, msg):
    pass


"""
The main function of this module, to be executed in a separate thread

Sets callbacks for specific topics, connects to the broker, then waits for incoming messages
"""
def main():
    global client

    if DBG:
        print(debugPrefix, "main")
        print("Just started; going to add callbacks, connect, and loop forever")
        print("")

    client = mqtt.Client(client_id=clientID)

    client.on_connect = on_connect
    client.message_callback_add(sub=storeyArrivalTopic, callback=handleStoreyArrival)
    client.on_message = on_message

    if DBG:
        print("Callbacks added; going to connect and loop forever")
        print("")
    # Will generate a CONNACK response from the server, triggering the on_connect() callback
    client.connect(brokerHost)

    if DBG:
        print("Connected; going to loop forever")
        print("")
    # Blocking function that automatically handles reconnection, and triggers the appropriate callback
    # for every incoming message
    client.loop_forever()
