#include <M5Stack.h>
#include <Wire.h>
#include <VL53L0X.h>
#include <TCA9548A.h>
VL53L0X sensor;
TCA9548A I2CMux; 

void setup() {
  Wire.begin();
  M5.begin();
  sensor.init();
  sensor.setTimeout(500);
  I2CMux.begin(Wire);             // Wire instance is passed to the library
  I2CMux.closeAll();              // Set a base state which we know (also the default state on power on)
}

void loop() {
int FL;
int FR;
int RF;
int RR;
  
  //if (!sensor.timeoutOccurred()) 

  I2CMux.openChannel(0);    // channel 0 open
    FL = sensor.readRangeSingleMillimeters();
    Serial.print("FL:");
    Serial.println(FL);
    M5.Lcd.setCursor(0, 0);
    M5.Lcd.println(FL);
  
  I2CMux.closeChannel(0);    // channel 0 close

  I2CMux.openChannel(1);    // channel 1 open
    FR = sensor.readRangeSingleMillimeters();
    Serial.print("FR:");
    Serial.println(FR);
    M5.Lcd.setCursor(0, 0);
    M5.Lcd.println(FR);
  
  I2CMux.closeChannel(1);    // channel 1 close

  I2CMux.openChannel(2);    // channel 1 open
    RF = sensor.readRangeSingleMillimeters();
    Serial.print("RF:");
    Serial.println(RF);
    M5.Lcd.setCursor(0, 0);
    M5.Lcd.println(RF);
  
  I2CMux.closeChannel(2);    // channel 1 close

  I2CMux.openChannel(3);    // channel 1 open
    RR = sensor.readRangeSingleMillimeters();
    Serial.print("RR:");
    Serial.println(RR);
    M5.Lcd.setCursor(0, 0);
    M5.Lcd.println(RR);
  
  I2CMux.closeChannel(3);    // channel 1 close
}
