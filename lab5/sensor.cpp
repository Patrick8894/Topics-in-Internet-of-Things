#include "Adafruit_GPS.h"
#include "PulseOximeter.h"
#include "DHT.h"

const int tempPin = A0;    // LM35
const int dhtPin = 4;    // LM393
const int poxPin = 2;     // Pulse Oximeter
Adafruit_GPS GPS;
PulseOximeter pox;
DHT dht(dhtPin);

void readTemperature() {
  int tempValue = analogRead(tempPin);
  float voltage = tempValue * (5.0 / 1023.0);
  Serial.print("Temperature: ");
  Serial.print(voltage * 100.0);
  Serial.println(" °C");
}

void readDHT() {
  bool isInCelcius = true;
  float h = dht.readHumidity() * 100;
  float temp = dht.readTemperature(isInCelcius); 
  Serial.print("Humidity: " + to_string(h) + "%; ");
  Serial.print("Temperature: " + to_string(temp) + "°C; ");
}

void readGPS() {
  if (Serial.available() > 0) {
    Serial.print("GPS: ");
    Serial.println(GPS.read());
  } else {
    Serial.println("Nothing from GPS.");
  }
}

void readPulseOximeter() {
  if (pox.begin()) {
    Serial.print("Heart rate:");
    Serial.print(pox.getHeartRate());
    Serial.print("bpm / SpO2:");
    Serial.print(pox.getSpO2());
    Serial.println("%");
  } else { 
    Serial.print("Nothing from pox.");
  }
}

void setup() {
  Serial.begin(9600);
  pox.begin();
  dht.begin();
  pinMode(dhtPin, INPUT);
  pinMode(poxPin, INPUT);
}

void loop() {
  readTemperature();
  readDHT();
  readGPS();
  readPulseOximeter();

  delay(1000);
}

