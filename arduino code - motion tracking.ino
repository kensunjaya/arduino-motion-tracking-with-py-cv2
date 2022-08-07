#include <Servo.h>

#define buzzerPin 8
#define laserPin 11

Servo servo_x;
Servo servo_y;

int sensitivity_x = 22; //Lower value = more sensitive
int sensitivity_y = 25; //Lower value = more sensitive

static int degree_x, degree_y, x_axis, y_axis;
static String b;


void setup() {
  pinMode(laserPin, OUTPUT);
  servo_x.attach(4);
  servo_y.attach(5);
  servo_x.write(95);
  servo_y.write(30);
  digitalWrite(laserPin, HIGH);

  Serial.begin(2000000); //set the baudrate to 2000000
  Serial.setTimeout(2);
}
 
void loop() {
  
  
  while(!Serial.available());
  
  b = Serial.readString();
  x_axis = b.substring(0, b.indexOf(" ")).toInt();
  y_axis = b.substring(b.indexOf(" ")+1).toInt();
  
  if ((x_axis + y_axis) != 0) {
 
    degree_x = x_axis/sensitivity_x;
    degree_y = y_axis/sensitivity_y;

    servo_x.write(52 + degree_x);
    servo_y.write(degree_y);

  }
  else {
    
    if (digitalRead(laserPin) == HIGH)
    digitalWrite(laserPin, LOW);
    else
    digitalWrite(laserPin, HIGH);
  }
  

  Serial.flush();
  
}
