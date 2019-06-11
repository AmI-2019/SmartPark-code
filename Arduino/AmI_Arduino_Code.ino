#include <SPI.h>
#include <Console.h>
#include <PubSubClient.h>
#include <YunClient.h>
#include <FastLED.h>
#include "SmartPark.h"                 // SmartPark is a proprietary library that allows for the usage of Sensor, Vehicle and Sequence objects, along with useful methods

#define BUZZER_PIN 2                   // the digital pin the buzzer is connected to
#define FREQUENCY 1000                 // the frequency (in Hz) for the buzzer sound
#define DURATION 50                    // the duration (in ms)of the buzzer sound - keep in mind: the tone() function doesn't stop the code while playing the sound!

#define LED_PIN 3                      // the digital pin the LED strip is connected to
#define MAX_PRES 2                     // the amount of presence sensors in the setup
#define MAX_SIDES 4                    // the amount of parking assistance sensors in the setup
#define NUM_LEDS 30                    // the total amount of LEDs in the setup
#define LED_TYPE WS2812B               // the LED strip type
#define COLOR_ORDER GRB                // the LED strip color order
#define MAX_MEX_SIZE 50                // the maximum number of bytes for the MQTT message
#define PORT 1883                      // the MQTT server port
#define MAX_ROAMING 3                  // the maximum number of vehicles that can move within the floor simultaneously

CRGB leds[NUM_LEDS];                       // an array to store the LEDs colors
CRGB leds_prio[NUM_LEDS][MAX_ROAMING+1];   // a matrix to manage the LEDs color priority
CRGB assignedCol[MAX_ROAMING];             // an array that allows for a static assignment of a color for each Vehicle object
CRGB off = CRGB::Black;                    

Sensor sensors[SENS_NUM];                  // an array of Sensor objects for optimal management of the IR sensors. The SENS_NUM constant equals the total number of physical sensors in the setup
Vehicle vehicles[MAX_ROAMING];             // an array of Vehicle objects to manage all the vehicles that are moving along the way to their spot simultaneously
Sequence seq;                              // an object to store the sequence sent by the MQTT broker

int8_t expected_sensors[MAX_ROAMING];      // an array to constantly keep track of which road sensors the system has to poll
uint8_t presence_sensors[MAX_PRES];        // an array to store the index of spot presence sensors
uint8_t parking_sensors[MAX_SIDES];        // an array to store the index of parking assistance sensors
uint8_t exit_sensor;                       // a variable to store the index of the exit sensor

IPAddress server(192,168,1,153);           // the MQTT server IP address
YunClient yun;
PubSubClient client(yun);                  // clients needed for MQTT communication

void callback(char* topic, byte* payload, unsigned int length)   // a function that is called whenever a MQTT message is received
{
	const unsigned int len = length;
	uint8_t assignedSpot;                                          // a variable to keep track of the spot that is assigned to the current vehicle
	uint8_t sensnum = 0;                                           // a variable we need to know how many sensors the vehicle has to cross to get to its spot
	uint8_t input[SENS_NUM + 1];                                    
  
	char *tokenIndex;
	char message[len];
  
	size_t index = 0;
  
	vec input_vec;
  
	for(unsigned int i = 0; i < length; i++)                       // saving the payload into a char array
	{
		message[i] = (char)payload[i]; 
	}
	
	tokenIndex = strtok(message,",");
	
	while((tokenIndex != nullptr)&&(index < SENS_NUM+1))           // converting the char array into a int array, formatted as following: {SPOT_NUMBER, SENSOR_1, SENSOR_2, ...}
	{
		sensnum+=1;
		input[index++] = atoi(tokenIndex);
		tokenIndex = strtok(NULL, ",");
	}
    
	for(uint8_t i = sensnum; i < SENS_NUM + 1; i++)                // setting all the remaining input values to -1, if any
	{
		input[i] = -1;
	}                                                             
	
	assignedSpot = input[0];                                       // the system stores the assigned spot 
	sensnum -=1;                                                   // the number of sensors has to be decremented because the first integer passed is not a sensor but the assigned spot
	Console.print("Assigned spot: ");                              // DEBUG prints
	Console.println(assignedSpot);
	Console.print("No. of sensors: ");
	Console.println(sensnum);
	Console.println("Sensors: ");
	
	for(uint8_t i = 1; i < sensnum+1; i++)                         // DEBUG prints
	{
		Console.print(input[i]);                                     
		Console.print(" ");
	}
	Console.println();
  
	for(uint8_t i = 0; i < SENS_NUM; i++)                          // storing the input array into a vec data structure
	{
		input_vec.v[i] = input[i+1];
	}
  
	seq.setLen(sensnum);                                           // storing the vec structure into a Sequence object
	seq.fill(input_vec);
  
	for(uint8_t i = 0; i < MAX_ROAMING; i++)                       // assigning a free Vehicle object to the vehicle
	{
		if(vehicles[i].isFree()) 
		{
			vehicles[i].assignFromSeq(seq);                            // storing the sequence of sensors and the assigned spot into the Vehicle object
			vehicles[i].updateSpot(assignedSpot);
			Console.print("Assigned Vehicle: ");                       // DEBUG prints
			Console.print(i);
			Console.print(" color: ");
			Console.println(assignedCol[i]);
			expected_sensors[i] = input[1];                            // updating the array that indicates which sensors the system should poll
			
			for(uint8_t j = 1; j < sensnum+1; j++)                     // adding the Vehicle object's color to the priority matrix for the LEDs assigned to the sensors the vehicle has to cross
			{               
				for(uint8_t k = 0; k < MAX_STRIP; k++) 
				{
					int led = sensors[input[j]].assignedLeds[k];
					
						for(uint8_t s = 0; s < MAX_ROAMING; s++) 
						{
							if(leds_prio[led][s]==off) 
							{
								leds_prio[led][s] = assignedCol[i];
								break;
							}
						}
          
				}
			}
			break;
		}	
	}
    
    
  
	Console.print("Sensors to poll: ");                            // DEBUG prints
	
	for(uint8_t h = 0; h < MAX_ROAMING; h++) 
	{
		Console.print(expected_sensors[h]);
		Console.print(" ");
	}
	Console.println();
}

void reconnect()                                         // this function is called immediately in the first loop and whenever the system loses connection to the MQTT server
{
	while (!client.connected())                            // the system will not return to the main code until it connects to it
	{                           
		Console.print("Attempting MQTT connection...");      
		if (client.connect("Arduino"))                       // trying to (re)connect to the server
		{               
			Console.println("connected");                        
			client.publish("arduino","yun connection test");   // once connected, the system publishes an announcement
			client.subscribe("strip/LED");                     // the system (re)subscribes to the strip/LED topic
		} else 
		{
			Console.print("failed, rc=");                      // if the connection attempt fails, retry every 5 seconds
			Console.print(client.state());
			Console.println(" try again in 5 seconds");          
			delay(5000);
		}
	}
}

void staticAssignment()                                  // this function hosts a mandatory list of static assignments of values; strictly demo-dependent
{
	sensors[0].assignedLeds[0] = 1;                        // manually assigning each LED to a sensor
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
	
	presence_sensors[0] =  9;                               // setting the number of the presence, parking assistance and exit sensors
	presence_sensors[1] = 10;
	parking_sensors[0] = 5;
	parking_sensors[1] = 6;
	parking_sensors[2] = 7;
	parking_sensors[3] = 8;
	exit_sensor = 11;
	
	assignedCol[0] = CRGB::Red;                             // assigning a different color to each Vehicle object                                    
	assignedCol[1] = CRGB::Blue;
	assignedCol[2] = CRGB::Green;
	
	for(uint8_t i = 0 ; i < SENS_NUM; i++)                  // assigning a different ADC pin to each Sensor object(from A0 to A11)
	{                         
		Sensor item(i+18);
		sensors[i] = item;
    }
	
	for(uint8_t i = 0; i < NUM_LEDS; i++)                   // initializing the LED priority matrix to 'off' (LED turned off)
	{
		for(uint8_t j = 0; j < MAX_ROAMING+1; j++) 
		{
			leds_prio[i][j] = off;
		}
    }
	
	for(uint8_t i = 0; i < MAX_ROAMING; i++)                // initializing the sensors the system has to poll to '-1' (as the sensor IDs range from 0 to 11, -1 means no sensor will be polled)
	{                  
		expected_sensors[i] = -1;
	}
}

void setup() 
{
	staticAssignment();                                                // calling the static assignment function
	FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);   // initializing the LED strip
	client.setServer(server,PORT);
	client.setCallback(callback);                                      // setting the server, port and callback values for the MQTT client
	Bridge.begin();                                                    // initializing the Yùn ethernet connection
	delay(3000);                                                   
	Console.begin();                                                   // initializing the Yùn LAN console output (for debug purpose)
	delay(2000);
	pinMode(BUZZER_PIN, OUTPUT);                                       // initializing the buzzer pin                         
	Console.println("Hardware ready.");                                // DEBUG print
}

void loop() 
{
	if (!client.connected())                                               // always check if the system is still connected
	{
		reconnect();
	}
	client.loop();                                                         // listening to MQTT messages
	for(uint8_t i = 0; i < MAX_ROAMING; i++)                               // road sensors polling start
	{      
		if(expected_sensors[i]!=-1)                                           
		{
			sensors[expected_sensors[i]].sense();                       
			if(sensors[expected_sensors[i]].isCrossed())                       // checking if the sensor is being crossed
			{         
				Console.print("sensor ");                                        // DEBUG prints
				Console.print(expected_sensors[i]);
				Console.println(" crossed!");
				
				for(uint8_t k = 0; k < MAX_STRIP; k++)                           // updating the color priority for the LEDs assigned to the crossed sensor
				{
					uint8_t led = sensors[expected_sensors[i]].assignedLeds[k];
					
					for(uint8_t h = 0; h < MAX_ROAMING; h++) 
					{
						leds_prio[led][h] = leds_prio[led][h+1];
					}
			  
				}
				vehicles[i].lastPosUpdate(expected_sensors[i]);                  // updating the last position of the vehicle to the sensor that has just been crossed
				expected_sensors[i] = vehicles[i].getNextPos();                  // updating the array of to-be-polled sensors with the next expected position of the vehicle
				if(vehicles[i].getNextPos() == -1)                               // if the next expected position of the vehicle equals -1, it means it reached its spot and therefore we can reset the Vehicle object
				{
					vehicles[i].reset();
				}
				Console.print("Sensors to poll: ");                              // DEBUG prints
				
				for(uint8_t h = 0; h < MAX_ROAMING; h++) 
				{
					Console.print(expected_sensors[h]);
					Console.print(" ");
				}
				Console.println();
			}
		}	   
	}                                                                      // road sensors polling end
  
	for(uint8_t i = 0; i < MAX_PRES; i++)                                  // spot presence sensors polling start
	{           
		uint8_t j = presence_sensors[i];
		sensors[j].sense();
		if(sensors[j].isSwitched())                                          // if the presence sensor changes its state, the system sends the MQTT broker a message
		{
			char tbuf[MAX_MEX_SIZE];
			char mbuf[MAX_MEX_SIZE];
      char mex;

			String topic = "storey/spot/" + String(sensor_to_spot(j));         // creating the topic to publish the message on
			if(sensors[j].getState()) 
			{
				mex = '1';
			} else 
			{
				mex = '0';
			}
			topic.toCharArray(tbuf,MAX_MEX_SIZE);
			client.publish(tbuf,mex);                                          // sending the message to the broker
		} 
	}                                                                      // spot presence sensors polling start                                                                                                                                                                
  
	for(uint8_t i = 0; i < MAX_SIDES; i++)                                 // parking assistance sensors polling start
	{
		uint8_t j = parking_sensors[i];
		if(sensors[j].rawIsCrossed()) 
		{
			tone(BUZZER_PIN, FREQUENCY, DURATION);
		}
	}                                                                      // parking assistance sensors polling end                                                       
  
	sensors[exit_sensor].sense();                                          // exit sensor polling start
	if(sensors[exit_sensor].isCrossed()) 
	{
		client.publish("storey/exit","AmI is awesome");
	}                                                                      // exit sensor polling end

	for(uint8_t i = 0; i < NUM_LEDS; i++)                                  // assigning each LED the highest priority color in the matrix
	{
		leds[i] = leds_prio[i][0];
	}

	FastLED.show();                                                        // updating the LED strip
}
