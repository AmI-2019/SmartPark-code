#include <SPI.h>
#include "SmartPark.h"

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
#define MAX_STRIP 10
CRGB leds[NUM_LEDS];                       // an array to store the LEDs colors
CRGB leds_prio[NUM_LEDS][MAX_ROAMING+1];   // a matrix to manage the LEDs color priority
CRGB assignedCol[MAX_ROAMING];

Sensor sensors[SENS_NUM]; 
Vehicle vehicles[MAX_ROAMING]; 
Sequence seq;                              // an object to store the sequence sent by the MQTT broker
int expected_sensors[MAX_ROAMING];
int led_chunk[SENS_NUM][MAX_STRIP];               // this matrix assigns each LED to a sensor
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
  Serial.print("Posto assegnato: ");                             // DEBUG prints
  Serial.println(assignedSpot);
  Serial.print("Numero sensori: ");
  Serial.println(sensnum);
  Serial.println("Sensori: ");
  for(unsigned int i = 1; i < SENS_NUM+1; i++) {
    Serial.println(input[i]);
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
      expected_sensors[i] = input[1];
      for(unsigned int j = 0; j < sensnum; j++) {                // put the Vehicle object's color in queue for the LEDs
        for(unsigned int k = 0; k < MAX_STRIP; k++) {
          if (leds_prio[led_chunk[j][k]][i] == CRGB(0,0,0)) {
            leds_prio[led_chunk[j][k]][i] = assignedCol[i];
            break;
          }
        }
      }
      break;
      
    }
    
  }
}
//const char server_test[] = "test.mosquitto.org"; // DEBUG - the test server URL
IPAddress server(192,168,0,38);                    // the server IP address
YunClient yun;
PubSubClient client(yun);                          // clients needed for MQTT communication

void reconnect() {
  while (!client.connected()) {                           // loop until we're reconnected
    Serial.print("Attempting MQTT connection...");
    if (client.connect("arduinoClient")) {                // attempt to connect
      Serial.println("connected");                        
      client.publish("outTopic","yun connection test");   // once connected, publish an announcement...
      client.subscribe("strip/LED");                      // ... and resubscribe
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");          
      delay(5000);
    }
  }
}

void setup() {
  assignedCol[0] = CRGB::Red;                                      // assigning a color to each Vehicle object
  assignedCol[1] = CRGB::Green;
  assignedCol[2] = CRGB::Blue;
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  Bridge.begin();
  client.setServer(server,PORT);
  client.setCallback(callback);
  delay(2000);                                                     // time required to the hardware to initialize everything
  Serial.begin(9600);                                              // DEBUG - serial output
  for(int i = 0 ; i < SENS_NUM; i++) {                             // This loop assigns an ADC pin to every Sensor object, starting from A0 up to A11.
    Sensor item(i+18);
    sensors[i] = item;
    pinMode(BUZZER_PIN, OUTPUT);
    // initialize leds_prio to CRGB(0,0,0)
    // initialize led_chunk (unused spaces are set to -1)
}
for(unsigned int i = 0; i < MAX_ROAMING; i++) {                    // expected sensors initialization
  expected_sensors[i] = 0;
}
}

void loop() {
if (!client.connected()) {
    reconnect();
  }
  client.loop();
  for(unsigned int i = 0; i < MAX_ROAMING; i++) {          // strip sensors polling
    sensors[expected_sensors[i]].sense();
    if(sensors[expected_sensors[i]].isCrossed()) {         // checks if a sensor is being crossed by a vehicle. The system only polls sensors that are expected to be crossed
      for(unsigned int j = 0; j < MAX_STRIP; j++) {
        for(unsigned int k = 0; k < MAX_ROAMING; k++) {    // updates the color priority for the LEDs associated to the current sensor
          leds_prio[led_chunk[expected_sensors[i]][j]][k] = leds_prio[led_chunk[expected_sensors[i]][j]][k+1]; 
        }
        leds[led_chunk[expected_sensors[i]][j]] = leds_prio[led_chunk[expected_sensors[i]][j]][0];             
      }                                                    // assigns the highest priority color to each LED (the value can also be 0 -> the LED turns off)
      vehicles[i].lastPosUpdate(expected_sensors[i]);
      expected_sensors[i] = vehicles[i].getNextPos();
      if(vehicles[i].getNextPos() == -1) {
        vehicles[i].reset();
        //Serial.println("veicolo arrivato al posto");
      }
      
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
  FastLED.show(); // update the LED strip
}
