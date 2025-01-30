#include <Wire.h>

#define SLAVE_ADDRESS 0x47 //I2C address of Arduino

void setup() {
  Wire.begin(SLAVE_ADDRESS); // Initialize as I2C slave
  Wire.onRequest(requestEvent); // Register callback for data requests
  Wire.onReceive(receiveEvent); // Register callback for data reception
  Serial.begin(115200);
}

void loop() {
  // Main code can run here
  delay(100);
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
