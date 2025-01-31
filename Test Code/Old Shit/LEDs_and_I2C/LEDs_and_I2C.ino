#include <Wire.h>
#define SLAVE_ADDRESS 0x08

#include <FastLED.h>
#define NUM_LEDS 30
#define DATA_PIN 5
#define DATA_PIN2 6
CRGB leds[NUM_LEDS];
#define TIME_FACTOR_HUE 60
#define TIME_FACTOR_SAT 100
#define TIME_FACTOR_VAL 100

String receivedString = ""; // To store the received string

void setup() {
  Wire.begin(SLAVE_ADDRESS); // Initialize as I2C slave
  Wire.onReceive(receiveEvent); // Register callback for data reception
  Serial.begin(115200);

  FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS / 2).setRgbw(RgbwDefault());
  FastLED.addLeds<WS2812, DATA_PIN2, GRB>(leds, NUM_LEDS / 2).setRgbw(RgbwDefault());
  FastLED.setBrightness(255);  // Set global brightness to max
  delay(2000);  // Allow upload delay
}

void loop() {
  // Main code for animations or other features can run here
  delay(100);
}

// Callback for when data is received from the master
void receiveEvent(int numBytes) {
  receivedString = ""; // Clear previous data
  while (Wire.available()) {
    char c = Wire.read(); // Read data
    receivedString += c;  // Append to string
  }
  Serial.println(receivedString); // Debug: Print received data

  // Check if the received string is "Red"
  if (receivedString.equalsIgnoreCase("Red")) {
    setLedsToColor(CRGB::Red); // Turn LEDs red
  }
}

// Function to set all LEDs to a specific color
void setLedsToColor(CRGB color) {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = color;
  }
  FastLED.show(); // Update the LEDs
}
