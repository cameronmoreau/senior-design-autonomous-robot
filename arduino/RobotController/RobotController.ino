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

int speed = 0;
int direction = 0;

void setup()
{
  SerialPortLeft.begin(9600);
  SerialPortLeft.listen();

  SerialPortRight.begin(9600);
  SerialPortRight.listen();

  Serial.begin(9600);
  delay(500);
  Serial.println("setup()");
  
  K1.start();
  K1.home().wait();
  K2.start();
  K2.home().wait();
  K3.start();
  K3.home().wait();
  K4.start();
  K4.home().wait();

    // Begin wheel spinning
  long minimum = K1.getMin().value();
  long maximum = K1.getMax().value();
  //long speed   = (maximum - minimum) / 10; // 1/10th of the range per second
  long speed = 200;
  
  
//  K1.s(speed).wait();
//  K2.s(speed).wait();
//  K3.s(-speed).wait();
//  K4.s(-speed).wait();
}

// .wait() waits until the command is 'finished'. For speed, this means it reached near the
// requested speed. You can also call K1.s(speed); without .wait() if you want to command it
// but not wait to get up to speed. If you do this, you may want to use K1.getS().value()
// to check progress.
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

void displayHeartbeat()
{
  Serial.printf("Speed %i, Direction %i\n", speed, direction);  
}

/**
 * changeMovement
 * Move the robot given a direction in degrees and speed to move
 * 
 * @param directionInput NULL or input of direction
 * @param speedInput NULL or speed to move
 */
void changeMovement(char *directionInput, char *speedInput)
{
  speed = 0, direction = 0;
  int adjusters[] = {1, 1, 1, 1};

  // Parse input
  if (directionInput != NULL) direction = atoi(directionInput);
  if (speedInput != NULL) speed = atoi(speedInput);

  // Temp direction 0 forward, 90 right, 180 back, 270 left
  if (direction == 0) { adjusters[2] = -1; adjusters[3] = -1; }
  else if (direction == 90) { adjusters[1] = -1; adjusters[2] = -1; }
  else if (direction == 180) { adjusters[0] = -1; adjusters[1] = -1; }
  else if (direction == 270) { adjusters[0] = -1; adjusters[3] = -1; }
  // temp
  else { speed = 0; }

  // Run motors
  K1.s(speed * adjusters[0]).wait();
  K2.s(speed * adjusters[1]).wait();
  K3.s(speed * adjusters[2]).wait();
  K4.s(speed * adjusters[3]).wait();

  Serial.printf("Updating movement: %d at speed %d\n", direction, speed);
}

void consumeIncommingMessage()
{
  int bytes = Serial.available();
  char * buffer = (char*)calloc(bytes, sizeof(char));

  // Read message
  Serial.readBytes(buffer, Serial.available());

  Serial.printf("Got data: %s\n", buffer);

  // Tokenize string
  int i = 0;
  char *split[] = {NULL, NULL, NULL};
  char *token = strtok(buffer, " ");
  while (token) {
    split[i++] = token;
    token = strtok(NULL, " ");  
  }

  if (split[0] != NULL) {
    if (strcmp(split[0], "h") == 0) displayHeartbeat();                       // r
    else if (strcmp(split[0], "r") == 0) Serial.println("TODO ROTATE");       // r <deg> <speed>
    else if (strcmp(split[0], "m") == 0) changeMovement(split[1], split[2]);  // m <direction> <speed>
  }

  free(buffer);  
}
