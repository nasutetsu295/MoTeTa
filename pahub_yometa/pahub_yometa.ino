#include <M5Stack.h>
#include <Wire.h>
#include <VL53L0X.h>

#include "ClosedCube_TCA9548A.h"

#define FRONT 2

#define X_LOCAL  100
#define Y_LOCAL  35
#define X_OFFSET 160
#define Y_OFFSET 34

#define PaHub_I2C_ADDRESS 0x70


VL53L0X sensor;
ClosedCube::Wired::TCA9548A tca9548a;

void setup() {
    M5.begin();
    M5.Power.begin();
    tca9548a.address(PaHub_I2C_ADDRESS);  // Set the I2C address.  设置I2C地址
    M5.Lcd.setTextFont(4);
    M5.Lcd.setCursor(70, 0, 4);
    M5.Lcd.setTextColor(YELLOW, TFT_BLACK);
    M5.Lcd.println(("PaHUB Example"));
    M5.Lcd.setTextColor(TFT_WHITE, TFT_BLACK);

     sensor.setTimeout(500);
  if (!sensor.init())
  {
    Serial.println("Failed to detect and initialize sensor!");
    while (1) {}
  }

#if defined LONG_RANGE
  // lower the return signal rate limit (default is 0.25 MCPS)
  sensor.setSignalRateLimit(0.1);
  // increase laser pulse periods (defaults are 14 and 10 PCLKs)
  sensor.setVcselPulsePeriod(VL53L0X::VcselPeriodPreRange, 18);
  sensor.setVcselPulsePeriod(VL53L0X::VcselPeriodFinalRange, 14);
#endif

#if defined HIGH_SPEED
  // reduce timing budget to 20 ms (default is about 33 ms)
  sensor.setMeasurementTimingBudget(20000);
#elif defined HIGH_ACCURACY
  // increase timing budget to 200 ms
  sensor.setMeasurementTimingBudget(200000);
#endif
}

void getdistance() {
    uint8_t returnCode = 0;
    uint8_t address;
    for (uint8_t channel = 0; channel < TCA9548A_MAX_CHANNELS; channel++) {

        returnCode = tca9548a.selectChannel(0);
        if (returnCode == 0) {

                Wire.beginTransmission(0x29);
                returnCode = Wire.endTransmission();
                if (returnCode == 0) {
                    Serial.print("I2C device = ");
                    Serial.printf("0X%X  ",0x29);
                      Serial.print(sensor.readRangeSingleMillimeters());
                      if (sensor.timeoutOccurred()) { Serial.print(" TIMEOUT"); }
                }
        }
                
        returnCode = tca9548a.selectChannel(1);
        if (returnCode == 0) {

                Wire.beginTransmission(0x29);
                returnCode = Wire.endTransmission();
                if (returnCode == 0) {
                    Serial.print("I2C device = ");
                    Serial.printf("0X%X  ",0x29);
                      Serial.print(sensor.readRangeSingleMillimeters());
                      if (sensor.timeoutOccurred()) { Serial.print(" TIMEOUT"); }


                }
        }

        returnCode = tca9548a.selectChannel(2);
        if (returnCode == 0) {

                Wire.beginTransmission(0x29);
                returnCode = Wire.endTransmission();
                if (returnCode == 0) {
                    Serial.print("I2C device = ");
                    Serial.printf("0X%X  ",0x29);
                      Serial.print(sensor.readRangeSingleMillimeters());
                      if (sensor.timeoutOccurred()) { Serial.print(" TIMEOUT"); }
                }
        }


        returnCode = tca9548a.selectChannel(3);
        if (returnCode == 0) {

                Wire.beginTransmission(0x29);
                returnCode = Wire.endTransmission();
                if (returnCode == 0) {
                    Serial.print("I2C device = ");
                    Serial.printf("0X%X  ",0x29);
                      Serial.print(sensor.readRangeSingleMillimeters());
                      if (sensor.timeoutOccurred()) { Serial.print(" TIMEOUT"); }

                }
        }

                returnCode = tca9548a.selectChannel(4);
        if (returnCode == 0) {

                Wire.beginTransmission(0x29);
                returnCode = Wire.endTransmission();
                if (returnCode == 0) {
                    Serial.print("I2C device = ");
                    Serial.printf("0X%X  ",0x29);
                      Serial.print(sensor.readRangeSingleMillimeters());
                      if (sensor.timeoutOccurred()) { Serial.print(" TIMEOUT"); }

                }
        }

  Serial.println();
                
            
        }
        delay(200);
    }



void loop(){
  getdistance();
}
