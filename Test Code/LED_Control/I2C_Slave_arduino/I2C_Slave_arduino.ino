#include <Wire.h>
#include <FastLED.h>

#define SLAVE_ADDRESS 0x47  // I2C address of the Arduino
#define NUM_LEDS 7
#define DATA_PIN 6

// Define a single array for the LED strip
CRGB leds[NUM_LEDS];

void setup() {
    Serial.begin(115200);       // Initialize serial for debugging
    Wire.begin(SLAVE_ADDRESS);  // Set I2C address
    Wire.onReceive(receiveData); // Register the I2C receive function

    FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS); // Configure LED strip
    FastLED.setBrightness(255);  // Set global brightness to max
    setLedsToColor(CRGB::White); // Initial color to white
}

void loop() {
    // Nothing needed here; LEDs update on I2C reception
}

// Function to set all LEDs to a specific color
void setLedsToColor(CRGB color) {
    for (int i = 0; i < NUM_LEDS; i++) {
        leds[i] = color;
    }
    FastLED.show(); // Update the LEDs
    Serial.println("LEDs updated");
}

// Function to receive integer data over I2C
void receiveData(int byteCount) {
    if (Wire.available()) {
        int receivedValue = Wire.read();  // Read the received integer
        Serial.print("Received: ");
        Serial.println(receivedValue);

        // Change LED color based on received value
        switch (receivedValue) {
            case 1:
                setLedsToColor(CRGB::Green);
                Serial.println("Set to Green");
                break;
            case 3:
                setLedsToColor(CRGB::Blue);
                Serial.println("Set to Blue");
                break;
            case 2:
                setLedsToColor(CRGB::Red);
                Serial.println("Set to Red");
                break;
            
            case 4:
                setLedsToColor(CRGB::White);
                Serial.println("Set to White");
                break;

            default:
                setLedsToColor(CRGB::White); // Default color
                Serial.println("Unknown value, set to White");
                break;
        }
    }
}
