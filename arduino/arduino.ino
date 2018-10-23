
char command = 0;

int PUL=11; //define Pulse pin
int DIR=2; //define Direction pin
int ENA=3; //define Enable Pin


void setup() {
    Serial.begin(9600);
pinMode (PUL, OUTPUT);
pinMode (DIR, OUTPUT);
pinMode (ENA, OUTPUT);


}

void loop() {

    command = Serial.read();
    if (command == 'd') {
        dispense();
    }
    delay(50);

} 

void dispense(){

  for (int i=0; i<3200; i++)    //Forward 5000 steps
  {
    digitalWrite(DIR,LOW);
    digitalWrite(ENA,HIGH);
    digitalWrite(PUL,HIGH);
    delayMicroseconds(50);
    digitalWrite(PUL,LOW);
    delayMicroseconds(50);
  }
    delay(5000);
  for (int i=0; i<3200; i++)   //Backward 5000 steps
  {
    digitalWrite(DIR,HIGH);
    digitalWrite(ENA,HIGH);
    digitalWrite(PUL,HIGH);
    delayMicroseconds(50);
    digitalWrite(PUL,LOW);
    delayMicroseconds(50);
  }
    delay(5000);

}


