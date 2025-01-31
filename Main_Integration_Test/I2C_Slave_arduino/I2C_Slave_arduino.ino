#include <Wire.h>
#include <FastLED.h>

#define SLAVE_ADDRESS 0x47  // I2C address of the Arduino
#define NUM_LEDS 7
#define DATA_PIN 6

// Define a single array for the LED strip
CRGB leds[NUM_LEDS];

bool chaseActive = false; // Flag for chase effect

void setup() {
    Serial.begin(115200);       // Initialize serial for debugging
    Wire.begin(SLAVE_ADDRESS);  // Set I2C address
    Wire.onReceive(receiveData); // Register the I2C receive function

    FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS); // Configure LED strip
    FastLED.setBrightness(255);  // Set global brightness to max
    setLedsToColor(CRGB::White); // Initial color to white
}

void loop() {
    if (chaseActive) {
        runChaseEffect(CRGB::White);  // Run chase effect in Blue
    }
}

// Function to set all LEDs to a specific color
void setLedsToColor(CRGB color) {
    chaseActive = false; // Stop chase effect
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
        leds[i] = CRGB::Red;
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
            case 2:
                setLedsToColor(CRGB::Red);
                Serial.println("Set to Red");
                break;
            case 3:
                setLedsToColor(CRGB::Blue);
                Serial.println("Set to Blue");
                break;
            case 4:
                setLedsToColor(CRGB::White);
                Serial.println("Set to White");
                break;
            case 5:
                chaseActive = true; // Enable chase effect
                Serial.println("Chase effect activated");
                break;
            default:
                setLedsToColor(CRGB::White); // Default color
                Serial.println("Unknown value, set to White");
                break;
        }
    }
}
