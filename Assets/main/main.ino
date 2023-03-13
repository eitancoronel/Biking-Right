
#include <LiquidCrystal_I2C.h>

//Constants:
const int potPinLeft = A0; //pin A0 to read analog input
const int potPinRight = A1; //pin A1 to read analog input

//Variables:
float left_value; //save analog value
float right_value; //save analog value
int high_score = 1;
LiquidCrystal_I2C lcd(0x3F,16,2);


void setup(){
    //Input or output
    Serial.begin(9600);
    lcdSetup();
    pinMode(potPinLeft, INPUT); //Optional
    pinMode(potPinRight, INPUT); //Optional

}

void lcdSetup(){
    lcd.init();
    lcd.clear();
    lcd.backlight();      // Make sure backlight is on

    lcd.setCursor(2,0);   //Set cursor to character 2 on line 0
    lcd.print("press the sensor!");

}

void printToLcd(float value,int x, int y){
    lcd.setCursor(0,1);
    lcd.print("L:");
    lcd.setCursor(8,1);
    lcd.print("R:");
    lcd.setCursor(x,y);
    lcd.print(value);
}

void print_left_val(){
    left_value = analogRead(potPinLeft);          //Read and save analog value from potentiometer
    left_value = map(left_value, 0, 1023, 0, 255); //Map value 0-1023 to 0-255 (PWM)
    // Serial.print("Left val: ");
    // Serial.print(millis());
    // Serial.print(", ");
    Serial.print(left_value);
    printToLcd(left_value,3, 1);
}
void print_right_val(){
    right_value = analogRead(potPinRight);          //Read and save analog value from potentiometer
    right_value = map(right_value, 0, 1023, 0, 255); //Map value 0-1023 to 0-255 (PWM)
    // Serial.print(", Right val: ");
    Serial.print(",");
    Serial.println(right_value);
    printToLcd(right_value,10, 1);
}

void loop(){
  lcd.clear();

    // if (left_value < high_score){
    //     lcd.clear();
    //    
    //     // lcd.setCursor(6,1);
    //     // lcd.print(value);
    //     // Serial.print(millis());
    //     // Serial.print(", ");
    //     Serial.println(left_value);
    // } else {
    //     high_score = left_value;
    //     lcd.setCursor(0,0);
    //     lcd.print("New high score!");
    //    printToLcd(left_value,6, 1);
    //     // lcd.setCursor(6,1);
    //     // lcd.print(value);
    //     // Serial.print("New high score: ");
    //     // Serial.print(millis());
    //     // Serial.print(", ");
    //     Serial.println(left_value);
    // }
    print_left_val();
    print_right_val();    
    delay(10);                          //Small delay

}