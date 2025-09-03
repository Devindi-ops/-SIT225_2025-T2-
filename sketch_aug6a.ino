#include <Arduino_LSM6DS3.h>  // Library for IMU sensors

void setup() {
  Serial.begin(9600);          // Start Serial communication
  while (!Serial);             // Wait for Serial port to connect (needed for Nano 33 IoT)
  
  if (!IMU.begin()) {          // Initialize IMU
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.println("timestamp_ms,x,y,z"); // CSV header for easier parsing
}

void loop() {
  float gx, gy, gz;

  // Check if gyroscope data is available
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(gx, gy, gz);  // Read x, y, z angular velocities
    
    unsigned long timestamp = millis();  // Current timestamp in milliseconds

    // Send data as CSV: timestamp,x,y,z
    Serial.print(timestamp);
    Serial.print(",");
    Serial.print(gx);
    Serial.print(",");
    Serial.print(gy);
    Serial.print(",");
    Serial.println(gz);
  }

  delay(100); // Sample every 100ms → 10Hz data rate (adjust as needed)
}
