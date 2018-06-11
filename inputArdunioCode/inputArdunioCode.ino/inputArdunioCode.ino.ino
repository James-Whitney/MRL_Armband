#define BUFFER 25

float out_0 = 512;
float out_1 = 512;
float out_2 = 512;

int iter = 0;

#include "TimerOne.h"

void setup()
{
  int i;
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(7, INPUT);

  Timer1.initialize(1000);
  Timer1.attachInterrupt(callback);

  Serial.begin(115200, SERIAL_8E1);              //  setup serial
}

void callback()
{
  out_0 += analogRead(A0);
  out_1 += analogRead(A1);
  out_2 += analogRead(A2);

  iter++;
  if(iter > 24) {
    iter = 0;
    Serial.print(out_0 / 25.0);
    Serial.print(" ");
    Serial.print(out_1 / 25.0);
    Serial.print(" ");
    Serial.println(out_2 / 25.0);
    out_0 = 0;
    out_1 = 0;
    out_2 = 0;
  }
}

void loop()
{

  // val_0[iter] = analogRead(A0);     // read the input pin
  // val_1[iter] = analogRead(A1);
  // val_2[iter] = analogRead(A2);
  // val_3[iter] = analogRead(A3);
  // iter++;
  // if(iter > BUFFER) {
  //   iter = 0;
  // }

  // Serial.print(avg_val(val_0));
  // Serial.print(" ");
  // Serial.print(avg_val(val_1));
  // Serial.print(" ");
  // Serial.print(avg_val(val_2));
  // Serial.print(" ");
  // Serial.println(avg_val(val_3));

  // out_0 = ((out_0 * 0.6) + (analogRead(A0) * 0.4));
  // out_1 = ((out_1 * 0.6) + (analogRead(A1) * 0.4));
  // out_2 = ((out_2 * 0.6) + (analogRead(A2) * 0.4));
  
  // Serial.print(out_0);
  // Serial.print(" ");
  // Serial.print(out_1);
  // Serial.print(" ");
  // Serial.println(out_2);
}
