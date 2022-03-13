const int BUFFER_SIZE = 4096;
char buf[BUFFER_SIZE];
const byte TRIG_BYTE = 47; // == "/"
const byte SEND_BYTE = 83; // == "S"
const byte READ_BYTE = 82; // == "R"


void setup() {
  Serial.begin(115200); // opens serial port, sets data rate to 115200 bps
}

void loop() {
  // check if data is available
  if (Serial.available() > 0) { 
    byte firstIncomingByte = Serial.peek(); // check first byte
    Serial.readBytes(buf, BUFFER_SIZE); // read all bytes

    if (firstIncomingByte == TRIG_BYTE) { 
      switch (buf[1]) {
        case SEND_BYTE: {
          Serial.print(buf); 
          break;
        }
        case READ_BYTE: {
          Serial.print("READ");
          break;
        }
      }
    } 

    // if (strcmp(buf, TRIGGER) == 0){
    //   Serial.println("Triggered"); 
    // } 

    while (Serial.read() >= 0) {}
    
    memset(buf, 0, sizeof(buf)); // clear buf variable 
  }
}
