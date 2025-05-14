#define HELTEC_POWER_BUTTON   // must be before "#include <heltec_unofficial.h>"
#include <heltec_unofficial.h>
#include "DHT.h"


#define PAUSE               300
#define FREQUENCY           905.2       // for US
#define BANDWIDTH           250.0
#define SPREADING_FACTOR    9
#define TRANSMIT_POWER      0

#define DHTPIN 4
#define DHTTYPE DHT22
#define SOUND_PIN 6

#define DEVICE_ID "esp32-01"
// #define DEVICE_ID "esp32-02"
// #define DEVICE_ID "esp32-03"

DHT dht(DHTPIN, DHTTYPE);

uint64_t last_tx = 0;
uint64_t tx_time;
uint64_t minimum_pause;

void setup() {
  Serial.begin(115200);

  heltec_setup();
  Serial.println("LoRa TX init");
  RADIOLIB_OR_HALT(radio.begin());
  Serial.printf("Frequency: %.2f MHz\n", FREQUENCY);
  RADIOLIB_OR_HALT(radio.setFrequency(FREQUENCY));
  RADIOLIB_OR_HALT(radio.setBandwidth(BANDWIDTH));
  RADIOLIB_OR_HALT(radio.setSpreadingFactor(SPREADING_FACTOR));
  RADIOLIB_OR_HALT(radio.setOutputPower(TRANSMIT_POWER));
  heltec_led(0);

  dht.begin();
  randomSeed(analogRead(0));
}

void loop() {
  heltec_loop();
  
  bool tx_legal = millis() > last_tx + minimum_pause;
  // Transmit a packet every PAUSE seconds or when the button is pressed
  if ((PAUSE && tx_legal && millis() - last_tx > (PAUSE * 1000)) || button.isSingleClick()) {
    // In case of button click, tell user to wait
    if (!tx_legal) {
      Serial.printf("Legal limit, wait %i sec.\n", (int)((minimum_pause - (millis() - last_tx)) / 1000) + 1);
      return;
    }
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
    // Maximum 1% duty cycle
    minimum_pause = tx_time * 100;
    last_tx = millis();
  }
}

String get_sensor_data() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int soundLevel = analogRead(SOUND_PIN);

  // Use this randomized mock data for lora experiment because my module has poor contact. I already have another demo video for collecting legit data.
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