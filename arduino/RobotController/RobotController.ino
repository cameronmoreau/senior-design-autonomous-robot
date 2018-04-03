// Speed Control Sample for Kangaroo
// Copyright (c) 2013 Dimension Engineering LLC
// See license.txt for license details.

#include <SoftwareSerial.h>
#include <Kangaroo.h>

// Arduino TX (pin 11) goes to Kangaroo S1
// Arduino RX (pin 10) goes to Kangaroo S2
// Arduino GND         goes to Kangaroo 0V
// Arduino 5V          goes to Kangaroo 5V (OPTIONAL, if you want Kangaroo to power the Arduino)
#define TX_PIN_LEFT 10
#define RX_PIN_LEFT 9
#define TX_PIN_RIGHT 1
#define RX_PIN_RIGHT 0

// Independent mode channels on Kangaroo are, by default, '1' and '2'.
SoftwareSerial  SerialPortLeft(RX_PIN_LEFT, TX_PIN_LEFT);
SoftwareSerial  SerialPortRight(RX_PIN_RIGHT, TX_PIN_RIGHT);
KangarooSerial  KLeft(SerialPortLeft);
KangarooSerial  KRight(SerialPortRight);
KangarooChannel K1(KLeft, '1');
KangarooChannel K2(KLeft, '2');
KangarooChannel K3(KRight, '1');
KangarooChannel K4(KRight, '2');

int speeds[] = {0, 0, 0, 0};

void setup()
{
  SerialPortLeft.begin(9600);
  SerialPortLeft.listen();

  SerialPortRight.begin(9600);
  SerialPortRight.listen();

  Serial.begin(9600);
  delay(500);
  Serial.println("setup()");

  // .wait() waits until the command is 'finished'. For speed, this means it reached near the
  // requested speed. You can also call K1.s(speed); without .wait() if you want to command it
  // but not wait to get up to speed. If you do this, you may want to use K1.getS().value()
  // to check progress.
  K1.start();
  K1.home().wait();
  K2.start();
  K2.home().wait();
  K3.start();
  K3.home().wait();
  K4.start();
  K4.home().wait();
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
    else if (strcmp(split[0], "g") == 0) Serial.println("TODO GRABBER");       // g
    else if (strcmp(split[0], "m") == 0) changeMovement(split[1], split[2], split[3], split[4]); // m <speed1> <speed2> <speed3> <speed4>
  }

  free(buffer);  
}
