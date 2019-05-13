import paho.mqtt.client as mqtt
import spots


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code ", str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    pass


brokerHost = "192.168.80.128"
clientID = "TargetDecision"

if __name__ == '__main__':

    client = mqtt.Client(client_id=clientID)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(brokerHost)

    client.loop_forever()