#include <Wire.h>
#include <FastLED.h>

// Pin arrangement:
// A0 pot and ~6 for main LED driver
// I2C - yellow A4, orange A5
// ~5 for LED strip data-line, 4 is second data line, possibly unused 

#define SLAVE_ADDRESS 0x47  // I2C address of the Arduino
#define NUM_LEDS 7
#define DATA_PIN 5 // Pin for LED strip data
#define PWM_PIN 6  // Main LED PWM pin
#define POT_PIN A0 // Potentiometer input
#define MAX_INPUT 200
#define POT_THRESHOLD 102

// Define a single array for the LED strip
CRGB leds[NUM_LEDS];

volatile uint8_t dutyCycle = 0;  // Stores received duty cycle value
volatile bool updatedViaI2C = false; // Flag to track update source
int lastPotValue = 0;  // Stores last potentiometer reading
bool chaseActive = false; // Flag for chase effect
bool potControlActive = false; // Flag to track if potentiometer is controlling

void setup() {
    Serial.begin(115200);       // Initialize serial for debugging
    Wire.begin(SLAVE_ADDRESS);  // Set I2C address
    Wire.onReceive(receiveData); // Register the I2C receive function

    FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS); // Configure LED strip
    FastLED.setBrightness(255);  // Set global brightness to max
    setLedsToColor(CRGB::White); // Initial color to white

    pinMode(PWM_PIN, OUTPUT);
    pinMode(POT_PIN, INPUT);
    lastPotValue = analogRead(POT_PIN);  // Initialize last potentiometer value
}

void loop() {
    int potValue = analogRead(POT_PIN);
    if (!updatedViaI2C || potControlActive || abs(potValue - lastPotValue) > POT_THRESHOLD) {  
        dutyCycle = map(potValue, 0, 1023, 1, 255); 
        updatedViaI2C = false;  // enable continuous pot adjustment
        potControlActive = true; // Set flag for pot control
        lastPotValue = potValue;  // Update last pot value only when taking control
    }
    analogWrite(PWM_PIN, dutyCycle);  // Set PWM output

    if (chaseActive) {
        runChaseEffect(CRGB::White);  // Run chase effect in White
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

        if (receivedValue >= 1 && receivedValue <= 5) {
            // LED Mode Control
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
            }
            // Main LED brightness values are given over I2C as 'Value + 100'
        } else if (receivedValue >= 101 && receivedValue <= 200) {
            // PWM Brightness Control
            dutyCycle = map(receivedValue - 100, 1, MAX_INPUT, 1, 255);  // Scale I2C value
            updatedViaI2C = true;
            potControlActive = false; // Reset pot control
            lastPotValue = analogRead(POT_PIN);  // Store last pot value when changing to I2C 
            Serial.print("PWM Updated to: ");
            Serial.println(dutyCycle);
        } else {
            setLedsToColor(CRGB::White); // Default color
            Serial.println("Unknown value, set to White");
        }
    }
}
