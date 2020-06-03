#include "TCS3200.h"
#include "SimpleKalmanFilter.h"
#define S0 4
#define S1 5 
#define S2 6
#define S3 7
#define sensorout 8
SimpleKalmanFilter KalmanFilter(2, 2, 0.001);
int red_value = 0;
int green_value = 0;
int blue_value = 0;
bool check = 0;
void setup() {
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(sensorout, INPUT);
  
  digitalWrite(S0,HIGH);
  digitalWrite(S1,LOW);
  Serial.begin(9600);
}
TCS3200 Sensor=TCS3200(S2, S3, sensorout);
void loop() {
  red_value = Sensor.getredvalue();
  delay(10);
  //red_value = KalmanFilter.updateEstimate(red_value);
  delay(200);

  green_value = Sensor.getgreenvalue();
  delay(10);
  //green_value = KalmanFilter.updateEstimate(green_value);
  delay(200);

  blue_value = Sensor.getbluevalue();
  delay(10);
  //blue_value = KalmanFilter.updateEstimate(blue_value);

  delay(200);
  Sensor.display(red_value, green_value, blue_value, check);

}

