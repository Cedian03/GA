#include <SPI.h>
#include <LoRa.h>

#define ss 5
#define rst 14
#define dio0 2

const int BUFFER_SIZE = 255;
byte buf[BUFFER_SIZE];

// assign the START_BYTE to be the first byte in your message
const char START_BYTE = '\b';

void setup() {
  // initialize Serial Monitor
  Serial.begin(115200); 
  while (!Serial);
  // Serial.println("LoRa Node");

  // setup LoRa transceiver module
  LoRa.setPins(ss, rst, dio0);

  // 433E6 for Asia
  // 866E6 for Europe
  // 915E6 for North America
  while (!LoRa.begin(866E6)) {
    // Serial.println(".");
    delay(500);
  }

  // change sync word (0xF3) to match the receiver
  // the sync word assures you don't get LoRa messages from other LoRa transceivers
  // ranges from 0-0xFF
  LoRa.setSyncWord(0x45);
  // Serial.println("LoRa Initializing OK!");
}

void loop() {
  // if serial data is available
  if (Serial.available() > 0) {
    // send START_BYTE
    LoRa.beginPacket();
    LoRa.write(START_BYTE);
    LoRa.endPacket();

    // while data is available send 255 bytes at a time
    while (Serial.available() > 0) {
      // read 255 bytes from serial port
      for (int i = 0; i < BUFFER_SIZE; i++) {
        buf[i] = Serial.read();
      }

      // send 255 bytes to LoRa
      LoRa.beginPacket();
      LoRa.write(buf, BUFFER_SIZE);
      LoRa.endPacket();
    }

    // send LoRa new line
    LoRa.beginPacket();
    LoRa.print("\n");
    LoRa.endPacket();
    }

  // try to parse packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // received a packet
    // Serial.print("Received packet: '");

    // read packet
    while (LoRa.available()) {
      String LoRaData = LoRa.readString();
      Serial.print(LoRaData); 
    }

    // print RSSI of packet
    // Serial.print("' with RSSI ");
    // Serial.println(LoRa.packetRssi());
  }

}
