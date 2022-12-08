#include <Servo.h>

#define laserPin 6
#define xPin 4
#define yPin 5

Servo servo_x;
Servo servo_y;

int degree_x, degree_y, x_axis, y_axis;
int sensitivity_x = 24; //Lower value = more sensitive
int sensitivity_y = 25; //Lower value = more sensitive

String pyData;


void attach_servo() {
  servo_x.attach(xPin);
  servo_y.attach(yPin);
}

/*
void detach_servo() {
  servo_x.detach();
  servo_y.detach();
}
*/

void setup() {
  pinMode(laserPin, OUTPUT);
  digitalWrite(laserPin, HIGH);
  
  attach_servo();
  servo_x.write(95);
  servo_y.write(30);
  
  Serial.begin(2000000);
  Serial.setTimeout(1);
}

void loop() {
  while(!Serial.available());
  
  pyData = Serial.readString();
  x_axis = pyData.substring(0, pyData.indexOf(" ")).toInt();
  y_axis = pyData.substring(pyData.indexOf(" ")+1).toInt();
    
  if ((x_axis + y_axis) <= 3000) {
    degree_x = x_axis/sensitivity_x;
    degree_y = y_axis/sensitivity_y;

    servo_x.write(50 + degree_x);
    servo_y.write(degree_y);
  }

  // Laser Functionality
  switch (x_axis + y_axis) {
    case 19998:   // Toggle laser
      if (digitalRead(laserPin) == HIGH) {
        digitalWrite(laserPin, LOW);
      }
      else {
        digitalWrite(laserPin, HIGH);
      }
      break;
    case 19996: // Turn off laser
      digitalWrite(laserPin, LOW);
      break;
    case 19997: // Turn on laser
      digitalWrite(laserPin, HIGH);
      break;
  }
  
  Serial.flush();
}
