from json import loads
from serial import Serial

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from util import ser_port
from util import ser_baudrate

def read(*args):
    with Serial(ser_port, ser_baudrate, timeout=1) as ser:
        if ser.out_waiting:
            print("Serial out not empty when sending", style="warning")

        incoming_bytes = ser.in_waiting
        line = ser.readline()
        print(incoming_bytes, line, ser.in_waiting)

def read_message():
    pass

def _dict_to_bytes(payload_bytes: bytes):
    payload_dict = loads(payload_bytes.decode())

    ciphertext_str = payload_dict["ciphertext"]
    signature_str = payload_dict["signature"]

    ciphertext_bytes = ciphertext_str.encode("latin1")
    signature_bytes = signature_str.encode("latin1")

    return ciphertext_bytes, signature_bytes

if __name__ == "__main__":
    read()
