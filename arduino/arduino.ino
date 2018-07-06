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

    command = Serial.read();
    if (command == 'v') {
        voicecheck();
    }
    if (command == 'd') {
        dispense();
    }
    delay(50);

} 

void dispense(){

    myservo.write(180);
    delay(5000);
    myservo.write(0);
    delay(5000);

}

void voicecheck(){

    soundCheck = 0;
    // Beginning of Start Voice Detection
    while(soundCheck < 7){
        // read the input on analog pin 0:
        int sensor = analogRead(A4);
        int sound = sensor - 400;

        //Peak detection
        if (sound < 90 || sound > 120) {
            i++;
        }
        delay(50);

        while (millis() - lastCheck > 1000) {

            if (i >= 1 && i < 4) {
                //Serial.println("Short word");
                word1++;
            } else if (i >= 4 && i < 10) {
                //Serial.println("Long word");
                word2++;
            }

            i = 0;
            lastCheck = millis();
            soundCheck++;
        }

        // Send to Pi after 7 secs
        if (soundCheck > 6) {

            Serial.println(word1);
            Serial.println(word2);

//            Serial.print(word1);
//            Serial.print(",");
//            Serial.println(word2);
            word1 = 0;
            word2 = 0;
        }
    }
    // End of Start Voice Detection
}
