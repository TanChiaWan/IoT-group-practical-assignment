#include "Timer.h"
#include <Servo.h>
#include <dht.h> 
#include <SPI.h>
#include <MFRC522.h>

//pins
const int RELAY_PIN = 2;
const int LED_AIRCOND_BLUE_PIN = 3;
const int DHT_PIN = 4;
const int LED_LIGHT_YELLOW_PIN = 7;
const int BUZZER_PIN = 8;
const int RST_PIN = 9;
const int SS_PIN = 10;

const int LDR_PIN = A0;
const int MICROPHONE_PIN = A2;
const int LED_PUNISHMENT_RED_PIN = A4;

//variables
int ldrStatus = 0;
float t;
float h;
int pos = 0;
String airCondStatus = "Off";
int noiseLevel = 0;
bool noiseDetect = false;
bool duringPunish = false;
bool punishTriggered = false;

String tagID = "";

bool electricity = false;

bool lighting = false;

//objects
MFRC522 mfrc522(SS_PIN, RST_PIN);
dht DHT;
Servo servo;
Timer timer;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  //rfid setup
  SPI.begin();
  mfrc522.PCD_Init();
  //mfrc522.PCD_DumpVersionToSerial();  // Show details of PCD - MFRC522 Card Reader details
  //Serial.println(F("Scan PICC to see UID, SAK, type, and data blocks..."));

  //pinMode
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_LIGHT_YELLOW_PIN, OUTPUT);
  pinMode(LED_AIRCOND_BLUE_PIN, OUTPUT);
  pinMode(LDR_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(MICROPHONE_PIN, INPUT);
  pinMode(LED_PUNISHMENT_RED_PIN, OUTPUT);

  //initialize
  digitalWrite(RELAY_PIN, LOW);
  servo.attach(5);

  for (int c = pos; c >= 0; c -=1) {
    servo.write(c);
    delay(15);
  }

}

void playSoundExit() {
  for (int i=0; i<2; i++) {
    tone(BUZZER_PIN, 1000); // Send 1KHz sound signal...
    delay(100);        // ...for 0.3 sec
    noTone(BUZZER_PIN);     // Stop sound...
    delay(100);        // ...for 0.3 sec
  }
}

void playSoundEnter() {
  tone(BUZZER_PIN, 1000);
  delay(100);
  noTone(BUZZER_PIN);
}

void playSoundNoAccess() {
  tone(BUZZER_PIN, 1000);
  delay(1500);
  noTone(BUZZER_PIN);
}

bool getID() {
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return false;
  }
  if (!mfrc522.PICC_ReadCardSerial()) {
    return false;
  }

  tagID = "";

  for (uint8_t i = 0; i < 4; i++) {
    tagID.concat(String(mfrc522.uid.uidByte[i], HEX));
  }

  tagID.toUpperCase();
  mfrc522.PICC_HaltA();
  return true;
}

void SmartLight() {
  ldrStatus = analogRead(LDR_PIN);
  //Serial.println(ldrStatus);
    if (ldrStatus <= 100 /*250*/) {
      digitalWrite(LED_LIGHT_YELLOW_PIN, HIGH); // If LDR senses darkness led pin high that means led will glow.
      lighting = true;
    }  
    else {
      digitalWrite(LED_LIGHT_YELLOW_PIN, LOW); // If LDR senses light led pin low that means led will stop glowing.
      lighting = false;
    }
}

void SmartAirCond() {
  int readDHTData = DHT.read11(DHT_PIN);

  t = DHT.temperature;        // Read temperature //22OC temperature & 57% humidity in A303 IoT lab
  h = DHT.humidity;           // Read humidity

  if (h > 70.00 || t > 25.00){
    digitalWrite(LED_AIRCOND_BLUE_PIN, HIGH);
    airCondStatus = "Strong";

    for (int c = pos; c <= 180; c +=1) {
      servo.write(c);
      delay(15);
    }

    pos = 180;
  }
  else if (h > 67.00 || t > 23.00) {
    digitalWrite(LED_AIRCOND_BLUE_PIN, HIGH);
    airCondStatus = "Weak";

    if (pos > 90) {
      for (int c = pos; c >= 90; c -=1) {
        servo.write(c);
        delay(15);
      }
    }

    if (pos < 90) {
      for (int c = pos; c <= 90; c +=1) {
        servo.write(c);
        delay(15);
      }
    }

    pos = 90;
  }
  else {
    digitalWrite(LED_AIRCOND_BLUE_PIN, LOW);
    airCondStatus = "Off";

    for (int c = pos; c >= 0; c -=1) {
      servo.write(c);
      delay(15);
    }

    pos = 0;
  }
}

void PunitiveAction() {
  noiseLevel = analogRead(MICROPHONE_PIN);

  if (duringPunish == false) {
    if (noiseLevel > 800) {
      duringPunish = true;
      punishTriggered = true;
      timer.oscillate(LED_PUNISHMENT_RED_PIN, 5000, HIGH);
    }
  }
}

void loop() {
  //control from python code and web dashboard
  if(Serial.available()) {
    int serialMsg = Serial.parseInt();

    switch(serialMsg) {
      case 1:
        electricity = true;
        playSoundEnter();
        break;
      case 2:
        electricity = true;
        playSoundExit();
        break;
      case 3:
        electricity = true;
        playSoundNoAccess();
        break;
      case 4:
        electricity = true; 
        break;
      case 5:
        electricity = false;
        playSoundEnter();
        break;
      case 6: 
        electricity = false;
        playSoundExit();
        break;
      case 7:
        electricity = false;
        playSoundNoAccess();
        break;
      case 8:
        electricity = false;
        break;
    }
    
  }

  if (electricity) {
    digitalWrite(RELAY_PIN, HIGH);
  }
  else {
    digitalWrite(RELAY_PIN, LOW);
  }

  //rfid

  if (getID()) {
    Serial.print(tagID);
  }
  else {
    Serial.print("no");
  }


  if (digitalRead(RELAY_PIN) == HIGH) {
    //ldr and led
    SmartLight();
    
    //dht11, led and servomotor
    SmartAirCond();

    //microphone sound and led
    PunitiveAction();
  }
  else {
    //off light
    digitalWrite(LED_LIGHT_YELLOW_PIN, LOW);
    
    //off aircond
    digitalWrite(LED_AIRCOND_BLUE_PIN, LOW);
    for (int c = pos; c >= 0; c -=1) {
      servo.write(c);
      delay(15);
    }
    pos = 0;

    ldrStatus = 0;
    t = 0.00;
    h = 0.00;
    airCondStatus = "Off";
    noiseLevel = 0;
  }

  //punishment
  if (duringPunish == true) {
    timer.update();
  }

  if (digitalRead(LED_PUNISHMENT_RED_PIN) == LOW) {
    duringPunish = false;
  }





  Serial.print(",");

  if (electricity == true) { //electricity
    Serial.print("On");
  }
  else {
    Serial.print("Off");
  }
  
  Serial.print(",");
  Serial.print(ldrStatus);
  Serial.print(",");

  if (lighting == true) { //lighting
    Serial.print("On");
  }
  else {
    Serial.print("Off");
  }

  Serial.print(",");
  Serial.print(t);
  Serial.print(",");
  Serial.print(h);
  Serial.print(",");
  Serial.print(airCondStatus); //air-cond
  Serial.print(",");
  Serial.print(noiseLevel);
  Serial.print(",");

  if (duringPunish == true) {
    Serial.print("Yes");
  }
  else {
    Serial.print("No");
  }

  Serial.print(",");
  if (punishTriggered == true) {
    Serial.println("Yes");
    punishTriggered = false;
  }
  else {
    Serial.println("No");
  }

  delay(500);

}
