from serial import Serial

PORT = input("PORT:")
BAUDRATE = 115200

with Serial(PORT, BAUDRATE, timeout=1) as ser:
    while True:
        if ser.in_waiting:
            print(ser.readline().decode().strip())