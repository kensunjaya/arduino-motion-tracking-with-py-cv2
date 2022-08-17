#include <Servo.h>

#define laserPin 11
#define resetPin 3

Servo servo_x;
Servo servo_y;

int degree_x, degree_y, x_axis, y_axis;
int sensitivity_x = 22; //Lower value = more sensitive
int sensitivity_y = 25; //Lower value = more sensitive

String b;


void attach_servo() {
  servo_x.attach(4);
  servo_y.attach(5);
}

/*
void detach_servo() {
  servo_x.detach();
  servo_y.detach();
}
*/

void setup() {
  digitalWrite(resetPin, HIGH);
  delay(200);
  pinMode(laserPin, OUTPUT);
  pinMode(resetPin, OUTPUT);
  attach_servo();
  servo_x.write(95);
  servo_y.write(30);
  digitalWrite(laserPin, HIGH);
  
  Serial.begin(2000000);
  Serial.setTimeout(2);
  delay(200);
}

void loop() {
  while(!Serial.available());
  
  b = Serial.readString();
  x_axis = b.substring(0, b.indexOf(" ")).toInt();
  y_axis = b.substring(b.indexOf(" ")+1).toInt();
  if ((x_axis + y_axis) <= 3000) {
    degree_x = x_axis/sensitivity_x;
    degree_y = y_axis/sensitivity_y;

    servo_x.write(52 + degree_x);
    servo_y.write(degree_y);

  }
  else if ((x_axis + y_axis) == 19998) { // Toggle Laser
    if (digitalRead(laserPin) == HIGH)
    digitalWrite(laserPin, LOW);
    else
    digitalWrite(laserPin, HIGH);
  }
  else if ((x_axis + y_axis) == 19996) { // Turn off Laser
    digitalWrite(laserPin, LOW);
  }
  else if ((x_axis + y_axis) == 19997) { // Turn on Laser
    digitalWrite(laserPin, HIGH);
  }
  else if ((x_axis + y_axis) == 19995) { // Reset board
    digitalWrite(resetPin, LOW);
  }
  
  Serial.flush();
}
