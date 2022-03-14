const int BUFFER_SIZE = 4096;
char buf[BUFFER_SIZE];

byte stored_messages[8]; 

const byte LINE_BYTE = 10; // == "\n"
const byte SEND_BYTE = 83; // == "S" 
const byte READ_BYTE = 82; // == "R" 
const byte CONF_BYTE = 67; // == "C"

void setup() {
  Serial.begin(115200); // opens serial port, sets data rate to 115200 bps
}

void loop() {
  // check if data is available
  if (Serial.available() > 0) { 
    byte firstByte = Serial.read(); // read first byte

    switch (firstByte) {
      case SEND_BYTE: {
        Serial.readBytesUntil(LINE_BYTE, buf, BUFFER_SIZE); 
        Serial.print(buf); 
        break;
      }
      case READ_BYTE: {
        Serial.print("READ");
        break;
      }
      case LINE_BYTE: {
        Serial.print("BEGINS WITH LINE_BYTE");
        break;
      }
    }


    // while (Serial.read() >= 0) {} // empty incoming serial data
    memset(buf, 0, BUFFER_SIZE); // clear buf variable // sizeof(buf)
  }
}
