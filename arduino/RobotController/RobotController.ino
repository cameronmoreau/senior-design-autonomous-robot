// Speed Control Sample for Kangaroo
// Copyright (c) 2013 Dimension Engineering LLC
// See license.txt for license details.

#include <SoftwareSerial.h>
#include <Servo.h>  
#include <Kangaroo.h>

// Arduino TX (pin 11) goes to Kangaroo S1
// Arduino RX (pin 10) goes to Kangaroo S2
// Arduino GND         goes to Kangaroo 0V
// Arduino 5V          goes to Kangaroo 5V (OPTIONAL, if you want Kangaroo to power the Arduino)
#define TX_PIN_LEFT 10
#define RX_PIN_LEFT 9
#define TX_PIN_RIGHT 1
#define RX_PIN_RIGHT 0

#define SERVO_PIN 16
#define SERVO_POS_UP 80
#define SERVO_POS_DOWN 170
#define MAGNET_PIN 18

// Independent mode channels on Kangaroo are, by default, '1' and '2'.
SoftwareSerial  SerialPortLeft(RX_PIN_LEFT, TX_PIN_LEFT);
SoftwareSerial  SerialPortRight(RX_PIN_RIGHT, TX_PIN_RIGHT);
KangarooSerial  KLeft(SerialPortLeft);
KangarooSerial  KRight(SerialPortRight);
KangarooChannel K1(KLeft, '1');
KangarooChannel K2(KLeft, '2');
KangarooChannel K3(KRight, '1');
KangarooChannel K4(KRight, '2');

// Servo
Servo servo;

// Global vars are great
int speeds[] = {0, 0, 0, 0};

void setup()
{
  // Setup Motor serial control
  SerialPortLeft.begin(9600);
  SerialPortLeft.listen();

  SerialPortRight.begin(9600);
  SerialPortRight.listen();

  // Setup Serial
  Serial.begin(9600);
  delay(500);
  Serial.println("setup()");

  // Setup Servo
  Serial.println("Init servo");
  servo.attach(SERVO_PIN);
  servo.write(SERVO_POS_DOWN);

  // Setup magnet
  Serial.println("Init magnet");
  pinMode(MAGNET_PIN, OUTPUT);

  // Init Motors
  Serial.println("Init motors");
  K1.start();
  K1.home().wait();
  K2.start();
  K2.home().wait();
  K3.start();
  K3.home().wait();
  K4.start();
  K4.home().wait();

  Serial.println("End setup");
}

void loop()
{
  // Send heartbeat message
  //displayHeartbeat();

  // Read any incoming messages
  if (Serial.available() > 0) {
    consumeIncommingMessage();
  }

  delay(200);
}

/**
 * Display a heardbeat and info messages
 */
void displayHeartbeat()
{
  Serial.printf("I'm alive. Speeds: %d %d %d %d\n", speeds[0], speeds[1], speeds[2], speeds[3]);  
}

/**
 * This method drives the 4 motors at individual speeds
 * 
 * @param si1 NULL or input of motor 1 speed
 * @param si2 NULL or input of motor 2 speed
 * @param si3 NULL or input of motor 3 speed
 * @param si4 NULL or input of motor 4 speed
 */
void changeMovement(char *si1, char *si2, char *si3, char *si4)
{
  // Reset global speeds to 0
  memset(speeds, 0, sizeof(speeds));
  
  // Input to speed
  if (si1 != NULL) speeds[0] = atoi(si1);
  if (si2 != NULL) speeds[1] = atoi(si2);
  if (si3 != NULL) speeds[2] = atoi(si3);
  if (si4 != NULL) speeds[3] = atoi(si4);

  // Run motors
  K1.s(speeds[0]).wait();
  K2.s(speeds[1]).wait();
  K3.s(speeds[2]).wait();
  K4.s(speeds[3]).wait();

  // Report
  Serial.printf("Manual speed wheels: %d %d %d %d\n", speeds[0], speeds[1], speeds[2], speeds[3]);
}

/**
 * changeArmServo
 * pos = 0 arm down
 * pos = 1 arm up
 * 
 * @parm pos NULL or input of arm position
 */
void changeArmServo(char *posInput) {
  int servoPos = SERVO_POS_DOWN;

  // Read arm inpu pos
  if (posInput != NULL) {
    int pos = atoi(posInput);

    // Put yo arms up, hommie
    if (pos == 1) servoPos = SERVO_POS_UP; 
  }
  Serial.printf("Arm at %d\n", servoPos);
  servo.write(servoPos);
}

/**
 * changeMagnet
 * input = 0 magnet disabled
 * input = 1 magnet enabled
 * 
 * @parm input NULL or input of magnet enabled
 */
void changeMagnet(char *input) {
  bool enabled = false;
  if (strcmp(input, "1") == 0) enabled = true;

  Serial.printf("Magnet at %d\n", enabled);
  if (enabled) digitalWrite(MAGNET_PIN, HIGH);
  else digitalWrite(MAGNET_PIN, LOW);
}

/**
 * Read serial input and run events
 */
void consumeIncommingMessage()
{
  int bytes = Serial.available();
  char * buffer = (char*)calloc(bytes, sizeof(char));

  // Read message
  Serial.readBytes(buffer, Serial.available());

  Serial.printf("Got data: %s\n", buffer);

  // Tokenize string
  int i = 0;
  char *split[] = {NULL, NULL, NULL, NULL, NULL};
  char *token = strtok(buffer, " ");
  while (token) {
    split[i++] = token;
    token = strtok(NULL, " ");  
  }

  if (split[0] != NULL) {
    if (strcmp(split[0], "h") == 0) displayHeartbeat();                       // h
    else if (strcmp(split[0], "a") == 0) changeArmServo(split[1]);            // a <pos>
    else if (strcmp(split[0], "g") == 0) changeMagnet(split[1]);              // g
    else if (strcmp(split[0], "m") == 0) changeMovement(split[1], split[2], split[3], split[4]); // m <speed1> <speed2> <speed3> <speed4>
  }

  free(buffer);  
}
