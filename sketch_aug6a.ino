const int ledPin = 3;
int incomingByte = 0;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    incomingByte = Serial.read(); // Read the byte
    if (incomingByte == '1') {
      digitalWrite(ledPin, HIGH); // Turn ON LED
    } else if (incomingByte == '0') {
      digitalWrite(ledPin, LOW);  // Turn OFF LED
    }
  }
}
