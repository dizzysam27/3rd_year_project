#include <Wire.h>
#include <FastLED.h>
#define SLAVE_ADDRESS 0x08

#define NUM_LEDS 7
#define DATA_PIN 6

// Define a single array for the LED strip
CRGB leds[NUM_LEDS];

String receivedColor = ""; // To store the received color string
bool chaseActive = false;  // Flag to track if the chase effect is active

void setup() {
  Serial.begin(115200);                  // Initialize serial for debugging
  Wire.begin(SLAVE_ADDRESS);                         // Set I2C address to 8
  Wire.onReceive(receiveData);           // Register the I2C receive function
  
  FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS);  // Configure LED strip
  FastLED.setBrightness(255);            // Set global brightness to max
  setLedsToColor(CRGB::White);           // Initial color to white
}

void loop() {
  // If chase effect is active, run the chase continuously
  if (chaseActive) {
    runChaseEffect(CRGB::Blue);  // Set to a color, can be changed
  }
}

// Function to set all LEDs to a specific color
void setLedsToColor(CRGB color) {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = color;
  }
  FastLED.show(); // Update the LEDs
  Serial.println("LEDs updated");
}

// Function to run the chase effect
void runChaseEffect(CRGB color) {
  static int currentLED = 0;

  // Reset all LEDs to off (Black)
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Black;
  }

  // Light up the current LED
  leds[currentLED] = color;

  // Move to the next LED
  currentLED++;

  // If we reach the end of the strip, start over
  if (currentLED >= NUM_LEDS) {
    currentLED = 0;
  }

  FastLED.show();  // Update the LEDs
  delay(100);      // Adjust speed of the chase
}

// Function to receive data from Raspberry Pi
void receiveData(int byteCount) {
  // Read the incoming data
  receivedColor = "";
  while (Wire.available()) {
    receivedColor += (char)Wire.read();
  }
  
  Serial.println("Received: " + receivedColor);  // Debugging info

  // Process received color and set LEDs
  if (receivedColor.equalsIgnoreCase("Red")) {
    setLedsToColor(CRGB::Red);
    chaseActive = false;
  } else if (receivedColor.equalsIgnoreCase("Green")) {
    setLedsToColor(CRGB::Green);
    chaseActive = false;
  } else if (receivedColor.equalsIgnoreCase("Blue")) {
    setLedsToColor(CRGB::Blue);
    chaseActive = false;
  } else if (receivedColor.equalsIgnoreCase("Chase")) {
    chaseActive = true;  // Activate chase effect
  } else {
    Serial.println("Unknown color received: " + receivedColor);
  }
}
