#include <SPI.h>
#include "SmartPark.h"
#include <Console.h>
#include <PubSubClient.h>
#include <YunClient.h>
#include <FastLED.h>
#define BUZZER_PIN 2
#define FREQUENCY 1000
#define DURATION 50
#define LED_PIN 3
#define MAX_PRES 2
#define MAX_SIDES 4
#define NUM_LEDS 30
#define LED_TYPE WS2812B
#define COLOR_ORDER GRB
#define MAX_MEX_SIZE 50                // the maximum number of bytes for the MQTT message
#define PORT 1883                      // the MQTT server port
#define MAX_ROAMING 3                  // the maximum number of vehicles that can move within the floor simultaneously
CRGB leds[NUM_LEDS];                       // an array to store the LEDs colors
CRGB leds_prio[NUM_LEDS][MAX_ROAMING+1];   // a matrix to manage the LEDs color priority
CRGB assignedCol[MAX_ROAMING];
CRGB off = CRGB::Black;

Sensor sensors[SENS_NUM]; 
Vehicle vehicles[MAX_ROAMING]; 
Sequence seq;                              // an object to store the sequence sent by the MQTT broker
int expected_sensors[MAX_ROAMING];
int presence_sensors[MAX_PRES];
int parking_sensors[MAX_SIDES];
const int exit_sensor;

void callback(char* topic, byte* payload, unsigned int length) { // a function called when a MQTT message is received
  const int len = length;
  char *tokenIndex;
  int assignedSpot;
  char message[len];
  int sensnum = 0;
  size_t index = 0;
  int input[SENS_NUM + 1];                                       // this array stores the assigned spot at index 0 and then the sequence of sensors the vehicle should cross
  
  vec input_vec;
  for(unsigned int i = 0; i < length; i++) {
    message[i] = (char)payload[i];
  }                                                              // the MQTT message is converted from a byte array to a char array
  tokenIndex = strtok(message,",");
  while((tokenIndex != nullptr)&&(index < SENS_NUM+1)) {         // this loop converts the message to a int array and stores it into input[]
    sensnum+=1;
    input[index++] = atoi(tokenIndex);
    tokenIndex = strtok(NULL, ",");
  }
  for(unsigned int i = sensnum; i < SENS_NUM + 1; i++) {
    input[i] = -1;
  }
  assignedSpot = input[0];                                       // the system stores the assigned spot 
  sensnum -=1;                                                   // the number of sensors has to be decremented because the first integer passed is not a sensor but the assigned spot
  Console.print("Assigned spot: ");                             // DEBUG prints
  Console.println(assignedSpot);
  Console.print("No. of sensors: ");
  Console.println(sensnum);
  Console.println("Sensors: ");
  for(unsigned int i = 1; i < sensnum+1; i++) {
    Console.println(input[i]);
  }
  for(unsigned int i = 0; i < SENS_NUM; i++) {                   // store the input sequence of sensors into a vec container (it doesn't include the spot number!)
    input_vec.v[i] = input[i+1];
  }
  seq.setLen(sensnum);                                           // store the sequence into a Sequence object
  seq.fill(input_vec);
  
  for(unsigned int i = 0; i < MAX_ROAMING; i++) {                // look for a free Vehicle object and assign the received data to it
    if(vehicles[i].isFree()) {
      vehicles[i].assignFromSeq(seq);
      vehicles[i].lastPosUpdate(0);
      vehicles[i].updateSpot(assignedSpot);
      Console.print("Assigned Vehicle: ");
      Console.print(i);
      Console.print(" color: ");
      Console.print(assignedCol[i]);
      expected_sensors[i] = input[1];
      for(unsigned int j = 1; j < sensnum+1; j++) {                // put the Vehicle object's color in queue for the LEDs
        for(unsigned int k = 0; k < MAX_STRIP; k++) {
          int led = sensors[input[j]].assignedLeds[k];
          for(unsigned int s = 0; s < MAX_ROAMING; s++) {
            if(leds_prio[led][s]==off) {
              leds_prio[led][s] = assignedCol[i];
              break;
            }
          }
          
        }
      }
      break;
      
    }
    
  }
  Console.print("Sensors to poll: ");
  for(unsigned int h = 0; h < MAX_ROAMING; h++) {
    Console.print(expected_sensors[h]);
    Console.print(" ");
  }
  Console.println();
}
//const char server_test[] = "test.mosquitto.org"; // DEBUG - the test server URL
IPAddress server(192,168,1,153);                    // the server IP address
YunClient yun;
PubSubClient client(yun);                          // clients needed for MQTT communication

void reconnect() {
  while (!client.connected()) {                           // loop until we're reconnected
    Console.print("Attempting MQTT connection...");
    if (client.connect("Arduino")) {                // attempt to connect
      Console.println("connected");                        
      client.publish("arduino","yun connection test");   // once connected, publish an announcement...
      client.subscribe("strip/LED");                      // ... and resubscribe
    } else {
      Console.print("failed, rc=");
      Console.print(client.state());
      Console.println(" try again in 5 seconds");          
      delay(5000);
    }
  }
}

void setup() {
  sensors[0].assignedLeds[0] = 1;
  sensors[0].assignedLeds[1] = 2;
  sensors[0].assignedLeds[2] = 3;

  sensors[1].assignedLeds[0] = 4;
  sensors[1].assignedLeds[1] = 5;
  sensors[1].assignedLeds[2] = 6;

  sensors[2].assignedLeds[0] = 7;
  sensors[2].assignedLeds[1] = 8;
  sensors[2].assignedLeds[2] = 9;

  sensors[3].assignedLeds[0] = 10;
  sensors[3].assignedLeds[1] = 11;
  sensors[3].assignedLeds[2] = 12;

  sensors[4].assignedLeds[0] = 13;
  sensors[4].assignedLeds[1] = 14;
  sensors[4].assignedLeds[2] = 15;
  
  
  delay(2000);
  assignedCol[0] = CRGB::Red;                                      // assigning a color to each Vehicle object
  assignedCol[1] = CRGB::Blue;
  assignedCol[2] = CRGB::Green;
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  client.setServer(server,PORT);
  client.setCallback(callback);
  Bridge.begin();
  delay(2000);                                                     // time required to the hardware to initialize everything
      Console.begin();
      delay(1000);
  Console.println("Hardware ready.");  
  pinMode(BUZZER_PIN, OUTPUT);                                     // DEBUG - serial output
  for(int i = 0 ; i < SENS_NUM; i++) {                             // This loop assigns an ADC pin to every Sensor object, starting from A0 up to A11.
    Sensor item(i+18);
    sensors[i] = item;
    
    for(unsigned int l = 0; l < NUM_LEDS; l++) {
      for(unsigned int j = 0; j < MAX_ROAMING+1; j++) {
        leds_prio[l][j] = CRGB::Black;
      }
    }
    
}
for(unsigned int i = 0; i < MAX_ROAMING; i++) {                    // expected sensors initialization
  expected_sensors[i] = -1;
}
}

void loop() {
  
if (!client.connected()) {
    reconnect();
  }
  client.loop();
  for(unsigned int i = 0; i < MAX_ROAMING; i++) {          // strip sensors polling
    if(expected_sensors[i]!=-1) {
    sensors[expected_sensors[i]].sense();
    if(sensors[expected_sensors[i]].isCrossed()) {         // checks if a sensor is being crossed by a vehicle. The system only polls sensors that are expected to be crossed
      Console.print("sensor ");
      Console.print(expected_sensors[i]);
      Console.println(" crossed!");
      for(unsigned int k = 0; k < MAX_STRIP; k++) {
          int led = sensors[expected_sensors[i]].assignedLeds[k];
          for(unsigned int h = 0; h < MAX_ROAMING; h++) {
            leds_prio[led][h] = leds_prio[led][h+1];
          }
          
      }
      vehicles[i].lastPosUpdate(expected_sensors[i]);
      expected_sensors[i] = vehicles[i].getNextPos();
      
      if(vehicles[i].getNextPos() == -1) {
        vehicles[i].reset();
        //Serial.println("veicolo arrivato al posto");
      }
      Console.print("Sensors to poll: ");
  for(unsigned int h = 0; h < MAX_ROAMING; h++) {
    Console.print(expected_sensors[h]);
    Console.print(" ");
  }
  Console.println();
    }
  }                                                        // strip polling end
  for(unsigned int i = 0; i < MAX_PRES; i++) {             // presence sensors polling
    sensors[presence_sensors[i]].sense();
    if(sensors[presence_sensors[i]].isSwitched()) {
      char tbuf[MAX_MEX_SIZE];
      char mbuf[MAX_MEX_SIZE];
      int mex;
      String topic = "storey/spot/" + String(sensor_to_spot(presence_sensors[i]));
      if(sensors[presence_sensors[i]].getState()) {
        mex = 0;
      } else {
        mex = 1;
      }
      char message = char(mex);
      topic.toCharArray(tbuf,MAX_MEX_SIZE);
      client.publish(tbuf,message);
    }
  }                                                        // presence polling end
  for(unsigned int i = 0; i < MAX_SIDES; i++) {            // parking sensors polling
    sensors[parking_sensors[i]].sense();
    if(sensors[parking_sensors[i]].isCrossed()) {
      tone(BUZZER_PIN, FREQUENCY, DURATION);
    }
  }                                                        // parking polling end
  sensors[exit_sensor].sense();
  if(sensors[exit_sensor].isCrossed()) {
    client.publish("storey/exit","AmI is awesome");
  }
  
}
for(unsigned int i = 0; i < NUM_LEDS; i++) {
  leds[i] = leds_prio[i][0];
}

FastLED.show(); // update the LED strip
}
