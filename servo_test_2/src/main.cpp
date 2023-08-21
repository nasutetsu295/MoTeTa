#include <M5Stack.h>

int FS90R = 21;

//PWMの設定
const double PWM_Hz = 50;     //PWM周波数
const uint8_t PWM_level = 16; //PWM 16bit(0～65535)

void setup() {
  Serial.begin(115200);

  M5.begin();
  M5.Lcd.setBrightness(100);
  M5.Lcd.setTextSize(2);
  M5.Lcd.setTextColor(WHITE, BLACK);

  pinMode(FS90R, OUTPUT);
  
  //モータのPWMのチャンネル、周波数の設定
  ledcSetup((uint8_t)1, PWM_Hz, PWM_level);

  //モータのピンとチャンネルの設定
  ledcAttachPin(FS90R, 1);
}
void loop() {
  //[FS90R]
  //1500～ 700usecで時計回り(CW)
  //1500～2300usecで反時計回り(CCW)
  //1500(±45)usecのときに停止。とはいうものの良くわからない(Hz?)ので実機で確認。

  // 4950 - 5050 を停止として、3000 - 7000 で稼働するようだ。
  // 3000 - 5000 で　時計回り、
  // 5000 - 7000 で反時計回り。
  
    ledcWrite(1, 3000);
    delay(260);

      ledcWrite(1, 5000);
          delay(1000);

    ledcWrite(1, 7000);
    delay(260);

       ledcWrite(1, 5000);
          delay(1000);     
}