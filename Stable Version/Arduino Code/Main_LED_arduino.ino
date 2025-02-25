#include <Wire.h>

#define PWM_PIN 9  // GPIO pin for PWM output
#define POT_PIN A0 // Analog pin for potentiometer input
#define MAX_INPUT 100
#define POT_THRESHOLD 102  // 10% of 1023 (full scale)

volatile uint8_t dutyCycle = 0;  // Stores received duty cycle value
volatile bool updatedViaI2C = false; // Flag to track update source
int lastPotValue = 0;  // Stores last potentiometer reading

void receiveEvent(int numBytes) {
    if (Wire.available()) {
        uint8_t receivedValue = Wire.read();
        if (receivedValue >= 1 && receivedValue <= MAX_INPUT) {
            dutyCycle = map(receivedValue, 1, MAX_INPUT, 1, 255);  // Scale to PWM range (1-255)
            updatedViaI2C = true;
        }
    }
}

void setup() {
    Wire.begin(8);  // Join I2C bus with address 8
    Wire.onReceive(receiveEvent);
    pinMode(PWM_PIN, OUTPUT);
    pinMode(POT_PIN, INPUT);
    lastPotValue = analogRead(POT_PIN);  // Initialize last potentiometer value
}

void loop() {
    int potValue = analogRead(POT_PIN);
    if (!updatedViaI2C || abs(potValue - lastPotValue) > POT_THRESHOLD) {  // Check for significant change
        dutyCycle = map(potValue, 0, 1023, 1, 255);  // Scale potentiometer input
        updatedViaI2C = false;  // Reset flag only if using potentiometer
    }
    analogWrite(PWM_PIN, dutyCycle);  // Set PWM output based on the latest duty cycle
    lastPotValue = potValue;  // Store last potentiometer reading
}
