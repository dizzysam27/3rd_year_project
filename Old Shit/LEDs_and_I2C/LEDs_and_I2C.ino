#include <Wire.h>
#define SLAVE_ADDRESS 0x47

#include <FastLED.h>
#define NUM_LEDS 30
#define DATA_PIN 6
#define DATA_PIN2 5
CRGB leds[NUM_LEDS];
#define TIME_FACTOR_HUE 60
#define TIME_FACTOR_SAT 100
#define TIME_FACTOR_VAL 100

void setup() {
  Wire.begin(SLAVE_ADDRESS); // Initialize as I2C slave
  Wire.onRequest(requestEvent); // Register callback for data requests
  Wire.onReceive(receiveEvent); // Register callback for data reception
  Serial.begin(9600);

  Serial.begin(115200);
  FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS/2).setRgbw(RgbwDefault());
  FastLED.addLeds<WS2812, DATA_PIN2, GRB>(leds, NUM_LEDS/2).setRgbw(RgbwDefault());
  FastLED.setBrightness(255);  // Set global brightness to 50%
  delay(2000);  // If something ever goes wrong this delay will allow upload.
}

void loop() {
  // Main code can run here
  delay(100);
  int32_t ms = millis();
  
  for(int i = 0; i < NUM_LEDS; i++) {
      // Use different noise functions for each LED and each color component
      uint8_t hue = inoise16(ms * TIME_FACTOR_HUE, i * 1000, 0) >> 8;
      uint8_t sat = inoise16(ms * TIME_FACTOR_SAT, i * 2000, 1000) >> 8;
      uint8_t val = inoise16(ms * TIME_FACTOR_VAL, i * 3000, 2000) >> 8;
      
      // Map the noise to full range for saturation and value
      sat = map(sat, 0, 255, 30, 255);
      val = map(val, 0, 255, 100, 255);
      
      leds[i] = CHSV(hue, sat, val);
    } 

    FastLED.show();
    
    // Small delay to control the overall speed of the animation
    //FastLED.delay(1);
}

// Callback for when data is requested by the master
void requestEvent() {
  Wire.write("Hello Pi!"); // Send a message
}

// Callback for when data is received from the master
void receiveEvent(int numBytes) {
  while (Wire.available()) {
    char c = Wire.read(); // Read data
    Serial.print(c);
  }
  Serial.println();
}
