#define BUFFER 25

float out_0 = 512;
float out_1 = 512;
float out_2 = 512;

int iter = 0;

void setup()
{
  int i;
  pinMode(A0, INPUT_PULLUP);
  pinMode(A1, INPUT_PULLUP);
  pinMode(A2, INPUT_PULLUP);
  pinMode(7, INPUT_PULLUP);
  Serial.begin(9600);              //  setup serial
}

void loop()
{
  /*
  val_0[iter] = analogRead(A0);     // read the input pin
  val_1[iter] = analogRead(A1);
  val_2[iter] = analogRead(A2);
  val_3[iter] = analogRead(A3);
  iter++;
  if(iter > BUFFER) {
    iter = 0;
  }

  Serial.print(avg_val(val_0));
  Serial.print(" ");
  Serial.print(avg_val(val_1));
  Serial.print(" ");
  Serial.print(avg_val(val_2));
  Serial.print(" ");
  Serial.println(avg_val(val_3));
  */
  out_0 = ((out_0 * 0.6) + (analogRead(A0) * 0.4));
  out_1 = ((out_1 * 0.6) + (analogRead(A1) * 0.4));
  out_2 = ((out_2 * 0.6) + (analogRead(A2) * 0.4));
  
  Serial.print(out_0);
  Serial.print(" ");
  Serial.print(out_1);
  Serial.print(" ");
  Serial.println(out_2);
}
