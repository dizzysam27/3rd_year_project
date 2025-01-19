#include <Wire.h>

#define SLAVE_ADDRESS 0x08 //I2C address of Arduino

void setup() {
  Wire.begin(SLAVE_ADDRESS); // Initialize as I2C slave
  Wire.onRequest(requestEvent); // Register callback for data requests
  Wire.onReceive(receiveEvent); // Register callback for data reception
  Serial.begin(9600);
}

void loop() {
  // Main code can run here
  delay(100);
}

// Callback for when data is received from the master
void receiveEvent(int numBytes) {
  while (Wire.available()) {
    char c = Wire.read(); // Read data
    Serial.print(c);
  }
  Serial.println();
}
