// Count the number of the short and long words
// Send to Pi after 5 secs silence
// If GPIO is HIGH, despense drink
// Written by Stanley Seow

#include <Servo.h>

Servo myservo;

int i = 0;
bool serialPlotter = 0;
unsigned long lastCheck;
unsigned long lastCheck2;
unsigned int word1;
unsigned int word2;
unsigned int soundCheck;
unsigned int passed;
unsigned int failed;

#define RED 9
#define GRN 10

void setup() {
  Serial.begin(9600);
  Serial.println("Detecting Sound Peaks V5");

  // Servo attached is pin11
  myservo.attach(11);

  // Move servo a bit to indicate servo is working
  myservo.write(0);
  delay(500);
  myservo.write(30);
  delay(500);
  myservo.write(0);

}

void loop() {

  // Beginning of Start Voice Detection
  if ( digitalRead ( 2 ) == LOW ) {
    Serial.println("STaRT");
  // read the input on analog pin 0:
  int sensor = analogRead(A4);

  int sound = sensor - 400;

  if ( sound < 90 || sound > 120  ) {
        i++;
        //Serial.print("Peak ");
  }
  delay(50);

  while ( millis() - lastCheck > 1000 ) {
    
    if ( i >= 1 && i < 4 ) {
      //Serial.println("Short word");
      word1++;
    } else if ( i >= 4 && i < 10 ) {
      //Serial.println("Long word");
      word2++;
    }

    i = 0;
    lastCheck = millis();
    soundCheck++;
  }

  // Send to Pi after 7 secs
  if ( soundCheck > 6  ) {
    // Print to RPI short words, long words
    Serial.print(word1);
    Serial.print(",");
    Serial.println(word2);
    word1 = 0;
    word2 = 0;
    soundCheck = 0;
    
  }

  } // End of Voice Detection


  // If D3 is HIGH, dispense drink
  if ( digitalRead( 3 ) == HIGH ) {

    myservo.write(180);
    delay(5000);
    myservo.write(0);
    delay(5000);
    Serial.println("*** Can dispensed");
  }

} // End of loop
