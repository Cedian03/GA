#include <SPI.h>
#include <LoRa.h>

#define ss 5
#define rst 14
#define dio0 2

const int BUFFER_SIZE = 4096;
char buf[BUFFER_SIZE];

void setup() {
  // initialize Serial Monitor
  Serial.begin(115200); 
  while (!Serial);
  Serial.println("LoRa Node");

  // setup LoRa transceiver module
  LoRa.setPins(ss, rst, dio0);

  // 433E6 for Asia
  // 866E6 for Europe
  // 915E6 for North America
  while (!LoRa.begin(866E6)) {
    Serial.println(".");
    delay(500);
  }

  // change sync word (0xF3) to match the receiver
  // the sync word assures you don't get LoRa messages from other LoRa transceivers
  // ranges from 0-0xFF
  LoRa.setSyncWord(0x45);
  Serial.println("LoRa Initializing OK!");
}

void loop() {
  // if data is available 
  if (Serial.available() > 0) {
    // read data
    Serial.readBytes(buf, BUFFER_SIZE); 
    
    Serial.print("Sending packet: ");
    Serial.println(buf); 
  
    // send LoRa packet to receiver
    LoRa.beginPacket();
    LoRa.print(buf);
    LoRa.endPacket();

    // empty buffer
    memset(buf, 0, BUFFER_SIZE);
  }

  // try to parse packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // received a packet
    Serial.print("Received packet: '");

    // read packet
    while (LoRa.available()) {
      String LoRaData = LoRa.readString();
      Serial.print(LoRaData); 
    }

    // print RSSI of packet
    Serial.print("' with RSSI ");
    Serial.println(LoRa.packetRssi());
  }

}

// const int BUFFER_SIZE = 4096;
// char buf[BUFFER_SIZE];

// byte stored_messages[8]; 

// const byte LINE_BYTE = 10; // == "\n"
// const byte SEND_BYTE = 83; // == "S" 
// const byte READ_BYTE = 82; // == "R" 
// const byte CONF_BYTE = 67; // == "C"

// void setup() {
//   Serial.begin(115200); // opens serial port, sets data rate to 115200 bps
// }

// void loop() {
//   // check if data is available
//   if (Serial.available() > 0) { 
//     byte firstByte = Serial.read(); // read first byte

//     switch (firstByte) {
//       case SEND_BYTE: {
//         Serial.readBytesUntil(LINE_BYTE, buf, BUFFER_SIZE); 
//         Serial.print(buf); 
//         break;
//       }
//       case READ_BYTE: {
//         Serial.print("READ");
//         break;
//       }
//       case LINE_BYTE: {
//         Serial.print("BEGINS WITH LINE_BYTE");
//         break;
//       }
//     }


//     // while (Serial.read() >= 0) {} // empty incoming serial data
//     memset(buf, 0, BUFFER_SIZE); // clear buf variable // sizeof(buf)
//   }
// }
