#include <Wire.h>

#define SLAVE_ADDRESS 0x47  // I2C address of the Arduino

void setup() {
    Wire.begin(SLAVE_ADDRESS);  // Start I2C as a slave
    Wire.onReceive(receiveData); // Register event for receiving data
    Wire.onRequest(sendData);   // Register event for sending data
    Serial.begin(115200);       // Start serial monitor
}

void loop() {
    // Empty loop - I2C runs via interrupts
}

// Function to handle incoming data from Raspberry Pi
void receiveData(int numBytes) {
    Serial.print("Bytes Received: ");
    Serial.println(numBytes);

    while (Wire.available()) {
        byte receivedByte = Wire.read();  // Read received byte
        Serial.print("Received from Raspberry Pi: ");
        Serial.println(receivedByte);
    }
}

// Function to send data when requested by Raspberry Pi
void sendData() {
    byte message = 42;  // Example data
    Wire.write(message);
    Serial.println("Sent to Raspberry Pi: 42");
}
