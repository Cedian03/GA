import sys
from threading import Thread
from time import sleep

from serial import Serial
from serial.tools.list_ports import comports

ports = comports()
for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))

PORT = input("PORT: ")
BAUDRATE = 115200
ser = Serial(PORT, BAUDRATE, timeout=1)

thread_running = True

def send():
    global thread_running

    while thread_running:
        inp = input().encode()
        if inp != b"":
            ser.write(inp)
        else:
            thread_running = False

def read():
    global thread_running 

    while thread_running:
        if ser.in_waiting:
            line = ser.readline().decode().strip()
            print(line)
        sleep(1)


if __name__ == '__main__':
    t1 = Thread(target=send)
    t2 = Thread(target=read)

    t1.start()
    t2.start()

    t2.join()  # interpreter will wait until your process get completed or terminated
    thread_running = False
    print('The end')
