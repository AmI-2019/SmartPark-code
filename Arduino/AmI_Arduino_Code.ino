#include "ami.h"
#include <SPI.h>
#include <PubSubClient.h>
#include <Bridge.h>
#include <BridgeClient.h>
#include <FastLED.h>

#define LED_PIN 3
#define NUM_LEDS 30
#define LED_TYPE WS2812B
#define COLOR_ORDER GRB
#define MAX_MEX_SIZE 50 // the maximum number of bytes for the MQTT message
#define PORT 1883 // the MQTT server port
#define SENS_NUM 12 // the total number of IR sensors in the system. 12 is the maximum value.
#define MAX_ROAMING 3 // the maximum number of vehicles that can move within the floor simultaneously
CRGB leds[NUM_LEDS];

Sensor sensors[SENS_NUM]; 
Vehicle vehicles[MAX_ROAMING]; 
vec numinput;
Sequence seq; // an object to store the sequence sent by the MQTT broker


void callback(char* topic, byte* payload, unsigned int length) { // a function called when a MQTT message is received
  String input = "";
  char input2[MAX_MEX_SIZE];
  const size_t buffersize = SENS_NUM;
  int buff[buffersize];
  int sensnum = 0;
  for(int i = 0; i < length; i++){
    char a = (char)payload[i];
      input += a;
      if(a == ',') {
        sensnum += 1;
      }
    }
  sensnum += 1;
  input.toCharArray(input2, MAX_MEX_SIZE);
  char *p = strtok(input2,",");
  size_t index = 0;
  while((p != nullptr)&&(index < buffersize)) {
    buff[index++] = atoi(p);
    p = strtok(NULL,",");
  }
  for(int i = 0; i < sensnum; i++) {
     numinput.v[i] = buff[i];
  }
  for(int i = sensnum; i < SENS_NUM; i++) {
    numinput.v[i] = -1;
  }
  seq.setLen(sensnum);
  seq.fill(numinput);
  int j = 0;
  while((j < MAX_ROAMING)&&(!vehicles[j].isFree())) { // look for the first Vehicle object that is not assigned to a vehicle yet
    j++;
  }
  if(j == MAX_ROAMING) {
  // handle the situation: no roaming vehicles slot available
  } else {
    vehicles[j].assignFromSeq(seq);      // the system assigns the passed sequence of sensors to a free Vehicle object
    Serial.println(vehicles[j].isFree());
  }
}
const char server[] = "test.mosquitto.org"; // the server IP/URL
BridgeClient yun;
PubSubClient client(yun); // clients needed for MQTT communication

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("arduinoClient")) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic","hello world - s246026");
      // ... and resubscribe
      client.subscribe("test_246");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  Bridge.begin();
  client.setServer(server,PORT);
  client.setCallback(callback);
  delay(2000); // time required to the hardware to initialize everything
  Serial.begin(9600); // DEBUG
  for(int i = 0 ; i < SENS_NUM; i++) { // This loop assigns an ADC pin to every Sensor object, starting from A0 up to A11.
    Sensor item(i+18);
    sensors[i] = item;
}
}

void loop() {
if (!client.connected()) {
    reconnect();
  }
  client.loop();
  // to-do: assign a different color to each active Vehicle object
  for(int i = 0; i < SENS_NUM; i++) { // sensors polling loop
    sensors[i].sense(); 
    if(sensors[i].isCrossed()) { // when a sensor is crossed, the system checks for a vehicle that is supposed to be there basing on its stored sequence and updates it
      for(int j = 0; j < MAX_ROAMING; j++) {
        if(!vehicles[j].isFree()) { // the system only cycles through Vehicles objects that are assigned to a vehicle
        int next = vehicles[j].getNextPos();
        if(next == -1) {
          // handle the situation: the vehicle has arrived to its spot
        } else if (next == i) {
          vehicles[j].lastPosUpdate(next); // updating the previous position to the current one
        }
        }
      }
      
    }
  } // polling end
  // write a loop to light up LEDs for each active Vehicle object
}
