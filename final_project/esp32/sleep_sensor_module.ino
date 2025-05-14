#define HELTEC_POWER_BUTTON   // must be before "#include <heltec_unofficial.h>"
#include <heltec_unofficial.h>
#include "DHT.h"

#define FREQUENCY           905.2       // for US
#define BANDWIDTH           250.0
#define SPREADING_FACTOR    9
#define TRANSMIT_POWER      0

#define STEEP_TIME          300

#define DHTPIN 4
#define DHTTYPE DHT22
#define SOUND_PIN 6

#define DEVICE_ID "esp32-01"
// #define DEVICE_ID "esp32-02"
// #define DEVICE_ID "esp32-03"

DHT dht(DHTPIN, DHTTYPE);

uint64_t tx_time;

void setup() {
  Serial.begin(115200);
  heltec_setup();

  Serial.println("LoRa Deep Sleep TX init");
  RADIOLIB_OR_HALT(radio.begin());
  RADIOLIB_OR_HALT(radio.setFrequency(FREQUENCY));
  RADIOLIB_OR_HALT(radio.setBandwidth(BANDWIDTH));
  RADIOLIB_OR_HALT(radio.setSpreadingFactor(SPREADING_FACTOR));
  RADIOLIB_OR_HALT(radio.setOutputPower(TRANSMIT_POWER));
  heltec_led(0);

  dht.begin();
  randomSeed(analogRead(0));

  delay(3000);

  String data = get_sensor_data();
  heltec_led(50); // 50% brightness is plenty for this LED
  tx_time = millis();
  RADIOLIB(radio.transmit(data));
  tx_time = millis() - tx_time;
  heltec_led(0);
  if (_radiolib_status == RADIOLIB_ERR_NONE) {
    Serial.printf("OK (%i ms)\n", (int)tx_time);
  } else {
    Serial.printf("fail (%i)\n", _radiolib_status);
  }
}

void loop() {
  heltec_loop();

  // Wait for button release, or it will wake us up again
  while (digitalRead(BUTTON) == LOW) {}
  delay (20);

  // Wake up on button press
  esp_sleep_enable_ext0_wakeup(BUTTON, LOW);

  heltec_deep_sleep(STEEP_TIME);
}

String get_sensor_data() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int soundLevel = analogRead(SOUND_PIN);

  // Use this randomized mock data for lora experiment because my sensor module has poor contact without soldering. 
  // I already have another demo video for collecting legit sensor data.
  temperature = 28.0 + random(-20, 21) / 10.0;
  humidity = 38.0 + random(-15, 16) / 10.0;
  soundLevel = 60 + random(-5, 6);

  String output = "Device: ";
  output += DEVICE_ID;
  output += " | Temp: ";
  output += String(temperature, 1);
  output += " °C, Humidity: ";
  output += String(humidity, 1);
  output += " %, Sound Level: ";
  output += String(soundLevel);

  Serial.println(output);
  return output;
}