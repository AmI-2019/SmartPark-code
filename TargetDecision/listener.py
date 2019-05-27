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
import spots
import arrival


brokerHost = "192.168.80.128"
clientID = "TargetDecision"
occupationTopic = "storey/spot/+"
entranceArrivalTopic = "entrance/plate"
storeyArrivalTopic = "storey/plate"
storeyExitTopic = "storey/exit"

"""
The callback for when the client receives a CONNACK response from the server.

Subscriptions are made here, so that they are automatically renewed at every reconnection.
"""
def on_connect(client, userdata, flags, rc):
    print("Connected with result code ", str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(occupationTopic)
    client.subscribe(entranceArrivalTopic)
    client.subscribe(storeyArrivalTopic)
    client.subscribe(storeyExitTopic)


"""
The callback for when a spot becomes occupied or free.

The message is structured as follows:
    Topic = '/storey/spot/<spotID>'
    Payload = occupation (0 | 1)

This event is handled by the 'spots' module.
"""
def handleOccupation(client, userdata, msg):
    topics = msg.topic.split("/")
    spotID = topics[2]
    # The payload needs to be decoded from binary to str, then converted to int
    occupiedAsInt = int(msg.payload.decode())

    # The second argument must be a bool
    spots.handleOccupation(spotID, occupiedAsInt == 1)


"""
The callback for when a new car approaches the entrance of the parking lot.

The message is structured as follows:
    Topic = '/storey/plate'
    Payload = plate number

This event is handled by the 'arrival' module.
"""
def handleEntranceArrival(client, userdata, msg):
    topics = msg.topic.split("/")
    plate = topics[1]

    # The second argument must be a bool
    arrival.handleEntranceArrival(plate)


"""
The callback for when a car approaches the entrance of the storey.

The message is structured as follows:
    Topic = /storey/plate
    Payload = plate number

This event is handled by the 'spots' module.
"""
def handleStoreyArrival(client, userdata, msg):
    plate = str(msg.payload.decode())

    spots.handleStoreyArrival(plate)


"""
The callback for when a car exits the storey.

The message is structured as follows:
    Topic = /storey/exit
    Payload = Empty

This event is handled by the 'spots' module.
"""
def handleStoreyExit(client, userdata, msg):
    spots.handleStoreyExit()


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
    client = mqtt.Client(client_id=clientID)

    client.on_connect = on_connect
    client.message_callback_add(sub=occupationTopic, callback=handleOccupation)
    client.message_callback_add(sub=entranceArrivalTopic, callback=handleEntranceArrival)
    client.message_callback_add(sub=storeyArrivalTopic, callback=handleStoreyArrival)
    client.message_callback_add(sub=storeyExitTopic, callback=handleStoreyExit)
    client.on_message = on_message

    # Will generate a CONNACK response from the server, triggering the on_connect() callback
    client.connect(brokerHost)

    # Blocking function that automatically handles reconnection, and triggers the appropriate callback
    # for every incoming message
    client.loop_forever()
