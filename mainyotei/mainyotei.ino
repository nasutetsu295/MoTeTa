#include <M5Stack.h>
#include <Wire.h>
#include <VL53L0X.h>

#include <TCA9548A.h>
#include <Wire.h>
#include "Free_Fonts.h"
#include "utility/CommUtil.h"

#include "ClosedCube_TCA9548A.h"

#define FRONT 2

#define SLAVE_ADDR        0x56
#define MOTOR_ADDR_BASE   0x00
#define ENCODER_ADDR_BASE 0x08
#define STEP_V            51

#define PaHub_I2C_ADDRESS 0x70


VL53L0X distancesensor;
ClosedCube::Wired::TCA9548A tca9548a; 
int16_t Speed = 0;
CommUtil Util;

int FL;
int FR;
int RF;
int RR;

int32_t ReadEncoder(uint8_t n) {
    uint8_t dest[4] = {0};

    if (n > 3) return 0;

    Util.readBytes(SLAVE_ADDR, ENCODER_ADDR_BASE + n * 4, 4, dest);

    return *((int32_t *)dest);
}

int32_t MotorRun(uint8_t n, int16_t Speed) {
    if (n > 3) return 0;

    if (Speed <= -255) Speed = -255;

    if (Speed >= 255) Speed = 255;

    Util.writeBytes(SLAVE_ADDR, MOTOR_ADDR_BASE + n * 2, (uint8_t *)&Speed, 2);

    return 1;
}

void kosen(){
  kouka
}

void setup() {
    M5.begin();
    M5.Power.begin();
    tca9548a.address(PaHub_I2C_ADDRESS);  // Set the I2C address.  设置I2C地址
    M5.Lcd.setTextFont(4);
    M5.Lcd.setCursor(70, 0, 4);
    M5.Lcd.setTextColor(YELLOW, TFT_BLACK);
    M5.Lcd.println(("PaHUB Example"));
    M5.Lcd.setTextColor(TFT_WHITE, TFT_BLACK);

     distancesensor.setTimeout(500);
    if (!distancesensor.init())
    {
      Serial.println("Failed to detect and initialize distancesensor!");
      while (1) {}
    }

  #if defined LONG_RANGE
    // lower the return signal rate limit (default is 0.25 MCPS)
    distancesensor.setSignalRateLimit(0.1);
    // increase laser pulse periods (defaults are 14 and 10 PCLKs)
    distancesensor.setVcselPulsePeriod(VL53L0X::VcselPeriodPreRange, 18);
    distancesensor.setVcselPulsePeriod(VL53L0X::VcselPeriodFinalRange, 14);
  #endif

  #if defined HIGH_SPEED
    // reduce timing budget to 20 ms (default is about 33 ms)
    distancesensor.setMeasurementTimingBudget(20000);
  #elif defined HIGH_ACCURACY
    // increase timing budget to 200 ms
    distancesensor.setMeasurementTimingBudget(200000);
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
                      Serial.print(distancesensor.readRangeSingleMillimeters());
                      if (distancesensor.timeoutOccurred()) { Serial.print(" TIMEOUT"); }
                }
        }
                
        returnCode = tca9548a.selectChannel(1);
        if (returnCode == 0) {

                Wire.beginTransmission(0x29);
                returnCode = Wire.endTransmission();
                if (returnCode == 0) {
                    Serial.print("I2C device = ");
                    Serial.printf("0X%X  ",0x29);
                      Serial.print(distancesensor.readRangeSingleMillimeters());
                      if (distancesensor.timeoutOccurred()) { Serial.print(" TIMEOUT"); }


                }
        }

        returnCode = tca9548a.selectChannel(2);
        if (returnCode == 0) {

                Wire.beginTransmission(0x29);
                returnCode = Wire.endTransmission();
                if (returnCode == 0) {
                    Serial.print("I2C device = ");
                    Serial.printf("0X%X  ",0x29);
                      Serial.print(distancesensor.readRangeSingleMillimeters());
                      if (distancesensor.timeoutOccurred()) { Serial.print(" TIMEOUT"); }
                }
        }


        returnCode = tca9548a.selectChannel(3);
        if (returnCode == 0) {

                Wire.beginTransmission(0x29);
                returnCode = Wire.endTransmission();
                if (returnCode == 0) {
                    Serial.print("I2C device = ");
                    Serial.printf("0X%X  ",0x29);
                      Serial.print(distancesensor.readRangeSingleMillimeters());
                      if (distancesensor.timeoutOccurred()) { Serial.print(" TIMEOUT"); }

                }
        }

                returnCode = tca9548a.selectChannel(4);
        if (returnCode == 0) {

                Wire.beginTransmission(0x29);
                returnCode = Wire.endTransmission();
                if (returnCode == 0) {
                    Serial.print("I2C device = ");
                    Serial.printf("0X%X  ",0x29);
                      Serial.print(distancesensor.readRangeSingleMillimeters());
                      if (distancesensor.timeoutOccurred()) { Serial.print(" TIMEOUT"); }

                }
        }

  Serial.println();
                
            
        }
        delay(200);
}

void motorstop(){
      MotorRun(1, 0);
    MotorRun(2, 0);
}

void turnright() {
  int   beforeencorder = ReadEncoder(2);
        while(ReadEncoder(2)<beforeencorder+1400){
          MotorRun(2,1300);
          MotorRun(3,-1300);        
          Serial.println(ReadEncoder(2));
      }
  motorstop();
}

void turnleft() {
  int   beforeencorder = ReadEncoder(2);
        while(ReadEncoder(2)>beforeencorder-1400){
          MotorRun(2,-1300);
          MotorRun(3,1300);        
          Serial.println(ReadEncoder(2));
      }
  motorstop();
}

void zenshin() {
  int   beforeencorder = ReadEncoder(2);
        while(ReadEncoder(2)<beforeencorder+2000){
          MotorRun(2,1300);
          MotorRun(3,1300);        
          Serial.println(ReadEncoder(2));
      }
  motorstop();
}

void loop(){
  getdistance();
  M5.update();

   if (RF < 150 &&  RR < 150)
  {
     if (FR < 200  && FL < 200)
     {
      //右壁前壁
      turnleft();
     }

    else {

      //右壁前なし
      // turnright();
      zenshin();

    }
  }
  else {

    //右なし前調べてない
    turnright();

    zenshin();
         
    M5.Lcd.print("ok5");
    }

  
  delay(1000);

}
