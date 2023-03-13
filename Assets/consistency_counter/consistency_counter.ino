#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x3F,16,2);

// Define the pin that the pressure sensor is connected to
const int leftSensorPin = A0;
const int rightSensorPin = A1;

// Define the threshold for detecting inconsistent pedaling
float pressureThreshold = 10;
const int minTreshold = 5;
const float tolarence = 0.7;


// Define the minimum time (in milliseconds) between sequential peaks
const int maxTimeThreshold = 1750;
const int minTimeThreshold = 500;
const int timeToResetLowPeak = 350;


// Define variables for storing the previous and current sensor readings
int beforeLastReading = 0;
int previousReading = 0;
int currentReading = 0;
int rightReading = 0;

// Define variables for storing the peak sensor value and time
int peakValue = 0;
unsigned long peakTime = 0;
bool low_peak = true;
bool isRested = true;
int peakCounter = 0; // Counter for the number of peaks achieved in a row
int highScore = 0;


const int movingAveregeRange = 10;
int movingAveregeData[movingAveregeRange] = {20,20,20,20,20,20,20,20,20,20};
const int colorAveregeRange = 30;
int colorAveregeData[colorAveregeRange] = {0};
int colorAverege = 0;

void setup() {
  // Initialize the serial communication
  Serial.begin(9600);
  lcdSetup();
}

void lcdSetup(){
    lcd.init();
    lcd.clear();
    lcd.backlight();      // Make sure backlight is on

    lcd.setCursor(0,0);   //Set cursor to character 2 on line 0
    lcd.print("press the sensor!");

}

void printToLcd(float value,int x, int y){
    lcd.setCursor(x,y);
    lcd.print(value);
}

void printToLcd(String value,int x, int y){
    lcd.setCursor(x,y);
    lcd.print(value);
}

float updateMovingAverege(int newVal, int range, int data[]) {
  float sum = newVal;
  for (int i = 0; i < range - 1; i++){
    data[i] = data[i + 1];
    sum += data[i];
  }
  data[range - 1] = newVal;
  return int(sum / range);
}

void calcColorAveregeByPeaks(){
  float sum = 0;
  for (int i = colorAveregeRange; i > 0 ; i--){
  sum += movingAveregeData[movingAveregeRange - i];
  }
}

void tests(){
  // print the values that the mooving averege is calculated from
  for (int i = 0; i < movingAveregeRange; i++){
    Serial.print(movingAveregeData[i]);
    Serial.print(", ");
  }
  Serial.print("curr tresh is : ");
  Serial.print(pressureThreshold * tolarence); // print effective treshold
  Serial.print(", color averege: ");
  Serial.print(colorAverege);  // print color average
  Serial.print(", left val is : ");
  Serial.print(currentReading);  // print curr val from left foot
  Serial.print(", right val is : ");
  Serial.print(rightReading);  // print curr val from right foot
  Serial.print(", counter is : ");
  Serial.println(peakCounter);
}

void updateHighScore(){
  if (peakCounter > highScore){
    highScore = peakCounter;
    printToLcd("high score: ",0, 0);
    printToLcd(highScore,12, 0);
    printToLcd(peakCounter,6, 1);
  }
}

void resetStreak(){
  peakCounter = 0;
  isRested = true;
  low_peak = true;
}

void loop() {

  // Read the left sensor reading
  currentReading = analogRead(leftSensorPin);
  // Read the right sensor reading
  rightReading = analogRead(rightSensorPin);

  int lastDiff = previousReading - beforeLastReading;
  int diff = currentReading - previousReading;

  colorAverege =  updateMovingAverege(previousReading,colorAveregeRange,colorAveregeData);

  if (diff < 0 && lastDiff > 0){
    if (previousReading > pressureThreshold * tolarence){
      int timeBetweensPeak = millis() - peakTime;
      bool correctTimeGap = timeBetweensPeak > minTimeThreshold && timeBetweensPeak < maxTimeThreshold;
      if(correctTimeGap || isRested){
        pressureThreshold = updateMovingAverege(previousReading,movingAveregeRange,movingAveregeData);
        peakTime = millis();
        isRested = false;
        peakCounter++;  
        updateHighScore();
      } else {
        resetStreak();
      }
    } 
  }
  tests();
  

  printToLcd(peakCounter,6, 1);
  if (millis() > peakTime + maxTimeThreshold){
    resetStreak();
  }
  beforeLastReading = previousReading;
  previousReading = currentReading;
  delay(10);
}
