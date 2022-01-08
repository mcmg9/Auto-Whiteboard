
#include <Servo.h>

int xPosition = 0;
int yPosition = 0;
int SW_state = 0;
int mapX = 0;
int mapY = 0;

int check = 0;

int minSpeedLeft = 63;
int minSpeedRight = 63;

int maxSpeedLeft = 120;
int maxSpeedRight = 120;

boolean inProgress = false;
boolean allReceived = false;

char tempBuffer[1500];

byte bytesRecvd = 0;

Servo servoLeft;
Servo servoRight;

void setup() {
  Serial.begin(115200);
  Serial.println("Ready");

  servoLeft.attach(10);
  servoRight.attach(9);

  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(2, INPUT_PULLUP);

  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {

  xPosition = analogRead(A0);
  yPosition = analogRead(A1);
  SW_state = digitalRead(2);
  mapX = map(xPosition, 0, 1023, -512, 512);
  mapY = map(yPosition, 0, 1023, -512, 512);

  Serial.println(mapX);
  Serial.println(mapY);

  if (mapX > 50) {
    if (mapY > 50) {
      servoLeft.attach(10);
      servoRight.detach();
      servoLeft.write(150);
      Serial.print("Up Left: ");
      //Serial.println(mapX);
    } else if (mapY < -50) {
      servoRight.attach(9);
      servoLeft.detach();
      servoRight.write(150);
      Serial.print("Down Left: ");
      //      Serial.println(mapX);
    } else {
      servoLeft.attach(10);
      servoRight.attach(9);
      servoLeft.write(150);
      servoRight.write(150);
      Serial.print("Left: ");
      Serial.println(mapX);
    }
  } else if (mapX < -50) {
    if (mapY > 50) {
      servoRight.attach(9);
      servoLeft.detach();
      servoRight.write(30);
      Serial.print("Up Right: ");
      //      Serial.println(mapX);
    } else if (mapY < -50) {
      servoLeft.attach(10);
      servoRight.detach();
      servoLeft.write(30);
      Serial.print("Down Right: ");
      //      Serial.println(mapX);
    } else {
      servoLeft.attach(10);
      servoRight.attach(9);
      servoLeft.write(30);
      servoRight.write(30);
      Serial.print("Right: ");
      //      Serial.println(mapX);
    }
  } else if (mapY > 50) {
    servoLeft.attach(10);
    servoRight.attach(9);
    servoLeft.write(150);
    servoRight.write(30);
    Serial.print("Up: ");
    //    Serial.println(mapY);
  } else if (mapY < -50) {
    servoLeft.attach(10);
    servoRight.attach(9);
    servoLeft.write(30);
    servoRight.write(150);
    Serial.print("Down: ");
    //    Serial.println(mapY);
  }

  if ((mapX > -50 && mapX < 50) && (mapY > -50 && mapY < 50) ) {
    servoLeft.detach();
    servoRight.detach();
  }

  if (Serial.available() > 0) {
    char x = Serial.read();

    if (x == 'U') {
      servoLeft.attach(10);
      servoRight.attach(9);
      servoLeft.write(maxSpeedLeft);
      servoRight.write(minSpeedRight);
    } else if (x == 'D') {
      servoLeft.attach(10);
      servoRight.attach(9);
      servoLeft.write(minSpeedLeft);
      servoRight.write(maxSpeedRight);
    } else if (x == 'L') {
      servoLeft.attach(10);
      servoRight.attach(9);
      servoLeft.write(maxSpeedLeft);
      servoRight.write(maxSpeedRight);
    } else if (x == 'R') {
      servoLeft.attach(10);
      servoRight.attach(9);
      servoLeft.write(minSpeedLeft);
      servoRight.write(minSpeedRight);
    } else if (x == 'E') {
      servoRight.attach(9);
      servoLeft.detach();
      servoRight.write(minSpeedRight);
    } else if (x == 'Q') {
      servoLeft.attach(10);
      servoRight.detach();
      servoLeft.write(maxSpeedLeft);
    } else if (x == 'C') {
      servoLeft.attach(10);
      servoRight.detach();
      servoLeft.write(minSpeedLeft);
    } else if (x == 'Z') {
      servoRight.attach(9);
      servoLeft.detach();
      servoRight.write(maxSpeedRight);
    }else if (x == "P"){
      Serial.end();
      Serial.begin(115200);
    }

    delay(100);
    
  }


  delay(50);
}
