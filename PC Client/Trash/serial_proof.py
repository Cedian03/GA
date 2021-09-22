#! /usr/bin/env python

"""Proof on Serial

Working with sketch_sep08c
"""

from time import sleep

import serial

COM_PORT = "COM7"

ser = serial.Serial(COM_PORT, 9600, timeout=1)

while True:
    val = input(">>>").encode('utf-8')
    ser.write(val + b"\n")
    sleep(.5)
    recived = ser.read_until("\n").decode("utf-8")
    print(recived)