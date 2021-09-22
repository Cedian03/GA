String incomingString; // for incoming serial data

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingString = Serial.readStringUntil("\n");

    // say what you got:
    Serial.print(incomingString);
  }
}
