
/*  Pulse Sensor Amped 1.5    by Joel Murphy and Yury Gitman   http://www.pulsesensor.com

  ----------------------  Notes ----------------------  ----------------------
  This code:
  1) Blinks an LED to User's Live Heartbeat   PIN 13
  2) Fades an LED to User's Live HeartBeat    PIN 5
  3) Determines BPM
  4) Prints All of the Above to Serial

  Read Me:
  https://github.com/WorldFamousElectronics/PulseSensor_Amped_Arduino/blob/master/README.md
  ----------------------       ----------------------  ----------------------
*/
// May 30,2018
// ESP32 version by coniferconifer
// https://github.com/WorldFamousElectronics/PulseSensor_Amped_Arduino/
// #define ESP32

#include "WiFi.h"
#include <PubSubClient.h>

const char* ssid = "POCOPHONE";
const char* pass = "david333";
const char* mqtt_server = "192.168.43.4";
const int port = 1883;
const String idArd = "ARD111";


WiFiClient espClient;
PubSubClient client(espClient);

String cutString(String string){
  int index1 = string.indexOf(',');
  String sender = string.substring(0, index1);
  int index2 = string.indexOf(',', index1+1);
  String pcktNum = string.substring(index1+1, index2);
  int index3 = string.indexOf(',', index2+1);
  String msg = string.substring(index2+1, index3);
  return msg;
}

String msgToSend(String string, String result){
  int index1 = string.indexOf(',');
  String sender = string.substring(0, index1);
  int index2 = string.indexOf(',', index1+1);
  String pcktNum = string.substring(index1+1, index2);
  int index3 = string.indexOf(',', index2+1);
  String msg = string.substring(index2+1, index3);
  int index4 = string.indexOf(',', index3+1);
  String timestamp = string.substring(index3+1, index4);

  String newStringToSend = idArd +","+ sender + "," + pcktNum + "," + result + "," + timestamp;
  Serial.println("Message Sending :" + newStringToSend);
  return newStringToSend;
}

void callback(char* topic, byte* payload, unsigned int length) {
 unsigned long time_start = millis();
 Serial.println();
 Serial.print("Message arrived [");
 Serial.print(topic);
 Serial.print("] ");
 String receivedChar = "";
 for (int i=0;i<length;i++) {
   receivedChar += (char)payload[i];
 }
 Serial.println(receivedChar);
 
 String request = cutString(receivedChar);//Separates the request
 String result = "Result";
 String messageToSend = msgToSend(receivedChar, result);

 char toSend[messageToSend.length()];
 messageToSend.toCharArray(toSend,messageToSend.length());
 
 delay(10);
 client.publish("debug2", toSend);
 unsigned long totat_time = millis()- time_start;
 
 Serial.println("-----------------------------------------------------------");
 Serial.println("Processing Time :" + String(totat_time) + "ms");
 Serial.println();
}

void sendShit(){
 String messageToSend = getStuf();
 char toSend[messageToSend.length()];
 messageToSend.toCharArray(toSend,messageToSend.length());
 
 delay(10);
 client.publish("Pulse", toSend);
 Serial.println("Sent" + String(messageToSend));
}
#define PROCESSING_VISUALIZER 1
#define SERIAL_PLOTTER  2

//  Variables
#define ESP32
#ifdef ESP32
#define LEDC_CHANNEL_0     0
#define LEDC_CHANNEL_1     1
#define LEDC_TIMER_8_BIT  8
#define LEDC_BASE_FREQ     5000
int pulsePin = 34;                 // Pulse Sensor purple wire connected to analog pin 34 , ADC6
int blinkPin = 13;                 // pin to blink led at each beat
int fadePin = 5;                  // pin to do fancy classy fading blink at each beat
int count = 0;
#else
int pulsePin = 0;                 // Pulse Sensor purple wire connected to analog pin 0
int blinkPin = 13;                // pin to blink led at each beat
int fadePin = 5;                  // pin to do fancy classy fading blink at each beat
#endif
int fadeRate = 0;                 // used to fade LED on with PWM on fadePin

// Volatile Variables, used in the interrupt service routine!
volatile int BPM;                   // int that holds raw Analog in 0. updated every 2mS
volatile int Signal;                // holds the incoming raw data
volatile int IBI = 600;             // int that holds the time interval between beats! Must be seeded!
volatile boolean Pulse = false;     // "True" when User's live heartbeat is detected. "False" when not a "live beat".
volatile boolean QS = false;        // becomes true when Arduoino finds a beat.

// SET THE SERIAL OUTPUT TYPE TO YOUR NEEDS
// PROCESSING_VISUALIZER works with Pulse Sensor Processing Visualizer
//      https://github.com/WorldFamousElectronics/PulseSensor_Amped_Processing_Visualizer
// SERIAL_PLOTTER outputs sensor data for viewing with the Arduino Serial Plotter
//      run the Serial Plotter at 115200 baud: Tools/Serial Plotter or Command+L
static int outputType = SERIAL_PLOTTER;
//static int outputType = PROCESSING_VISUALIZER;

void setup() {
  pinMode(blinkPin, OUTPUT);        // pin that will blink to your heartbeat!
  pinMode(fadePin, OUTPUT);         // pin that will fade to your heartbeat!
  Serial.begin(115200);             // we agree to talk fast!

    WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
 
  Serial.println("WiFi connected with IP:");
  Serial.println(WiFi.localIP());

  client.setServer(mqtt_server, port);
  client.setCallback(callback);
  interruptSetup();                 // sets up to read Pulse Sensor signal every 2mS
  // IF YOU ARE POWERING The Pulse Sensor AT VOLTAGE LESS THAN THE BOARD VOLTAGE,
  // UN-COMMENT THE NEXT LINE AND APPLY THAT VOLTAGE TO THE A-REF PIN
  //   analogReference(EXTERNAL);
#ifdef ESP32
  ledcSetup(LEDC_CHANNEL_0, LEDC_BASE_FREQ, LEDC_TIMER_8_BIT) ; // 8bit precision
  ledcAttachPin(fadePin, LEDC_CHANNEL_0) ; // assaign LED1 to CH0
#endif


}


//  Where the Magic Happens
void loop() {
   if(WiFi.status() != WL_CONNECTED){
      reconnect();
    }
 
    if (!client.connected()) {
      reconnectMQTT();
    }

    client.loop();
  
  //serialOutput() ;
  count++;
  if (count == 50){
    count = 0;
    sendShit();
  }
  if (QS == true) {    // A Heartbeat Was Found
    // BPM and IBI have been Determined
    // Quantified Self "QS" true when arduino finds a heartbeat
    fadeRate = 255;         // Makes the LED Fade Effect Happen
    // Set 'fadeRate' Variable to 255 to fade LED with pulse
    serialOutputWhenBeatHappens();   // A Beat Happened, Output that to serial.
    QS = false;                      // reset the Quantified Self flag for next time
  }

  ledFadeToBeat();                      // Makes the LED Fade Effect Happen
  delay(100);                             //  take a break
}

void ledFadeToBeat() {
  fadeRate -= 15;                         //  set LED fade value
  fadeRate = constrain(fadeRate, 0, 255); //  keep LED fade value from going into negative numbers!
#ifdef ESP32
  ledcWrite(LEDC_CHANNEL_0, fadeRate) ;
#else
  analogWrite(fadePin, fadeRate);         //  fade LED
#endif
}

void reconnect(){
  WiFi.begin(ssid, pass);
   while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Reconnecting to WiFi..");
   }
   Serial.println("WiFi reconnected with IP:");
   Serial.println(WiFi.localIP());
}

void reconnectMQTT() {
 // Loop until we're reconnected
 while (!client.connected()) {
 Serial.print("Attempting MQTT connection...");
 // Attempt to connect
 if (client.connect("ESP32 Client")) {
  Serial.println("connected");
  // ... and subscribe to topic
  client.subscribe("debug");
  client.subscribe("*");
 } else {
  Serial.print("failed, rc=");
  Serial.print(client.state());
  Serial.println("try again in 5 seconds");
  // Wait 5 seconds before retrying
  delay(5000);
  }
 }
}
