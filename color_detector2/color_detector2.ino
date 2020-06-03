
// Define color sensor pins
 
#define S0 4
#define S1 5
#define S2 6
#define S3 7
#define sensorOut 8
#include "SimpleKalmanFilter.h"
 
// Calibration Values
// Get these from Calibration Sketch
SimpleKalmanFilter KalmanFilter(2, 2, 0.001);
int redMin = 45;  // Do cac gia tri Min max ban dau
int redMax = 220;  // cua 3 mau de map gia tri 0->255 tuong ung 
int greenMin = 47; // voi min -> max
int greenMax = 248; 
int blueMin = 38; 
int blueMax =172; 
// Variables for Color Pulse Width Measurements
 
int redPW = 0;
int greenPW = 0;
int bluePW = 0;
 
// Variables for final Color values
 
int redValue;
int greenValue;
int blueValue;
 
void setup() {
 
  // Set S0 - S3 as outputs
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  
  // Set Sensor output as input
  pinMode(sensorOut, INPUT);
  
  // Set Frequency scaling to 20%
  digitalWrite(S0,HIGH);
  digitalWrite(S1,LOW);
  
  // Setup Serial Monitor
  Serial.begin(9600);
}
 
void loop() {
  
  // Read Red value
  redPW = getRedPW();
  //redPW = KalmanFilter.updateEstimate(redPW);
  // Map to value from 0-255
  redValue = norm(map(redPW, redMin,redMax,255,0));
  // Delay to stabilize sensor
  delay(200);
  
  // Read Green value
  greenPW = getGreenPW();
  //greenPW = KalmanFilter.updateEstimate(greenPW);
  // Map to value from 0-255
  greenValue = norm(map(greenPW, greenMin,greenMax,255,0));
  // Delay to stabilize sensor
  delay(200);
  
  // Read Blue value
  bluePW = getBluePW();
  //bluePW = KalmanFilter.updateEstimate(bluePW);
  // Map to value from 0-255
  blueValue = norm(map(bluePW, blueMin,blueMax,255,0));
  // Delay to stabilize sensor
  delay(200);
  
  // Print output to Serial Monitor
  Serial.print("Red = ");
  Serial.print(redValue);
  Serial.print(" - Green = ");
  Serial.print(greenValue);
  Serial.print(" - Blue = ");
  Serial.println(blueValue);
  
}
 
 
// Function to read Red Pulse Widths
int getRedPW() {
 
  // Set sensor to read Red only
  digitalWrite(S2,LOW);
  digitalWrite(S3,LOW);
  // Define integer to represent Pulse Width
  int PW;
  // Read the output Pulse Width
  PW = pulseIn(sensorOut, LOW);
  // Return the value
  return PW;
 
}
 
// Function to read Green Pulse Widths
int getGreenPW() {
 
  // Set sensor to read Green only
  digitalWrite(S2,HIGH);
  digitalWrite(S3,HIGH);
  // Define integer to represent Pulse Width
  int PW;
  // Read the output Pulse Width
  PW = pulseIn(sensorOut, LOW);
  // Return the value
  return PW;
 
}
 
// Function to read Blue Pulse Widths
int getBluePW() {
 
  // Set sensor to read Blue only
  digitalWrite(S2,LOW);
  digitalWrite(S3,HIGH);
  // Define integer to represent Pulse Width
  int PW;
  // Read the output Pulse Width
  PW = pulseIn(sensorOut, LOW);
  // Return the value
  return PW;
 
}

int norm(int value)
{
  if (value > 255)
    return 255;
  else if (value < 0 )
    return 0;
  else 
    return value;
}
