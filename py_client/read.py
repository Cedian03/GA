from json import loads
from serial import Serial
from time import sleep

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from util import SER_PORT
from util import SER_BAUDRATE
from util import PRIVATE_KEY


def read_messages(*args):
    with Serial(SER_PORT, SER_BAUDRATE, timeout=1) as ser:
        if ser.out_waiting:
            print("Serial out not empty when sending", style="warning")

        incoming_bytes = ser.in_waiting
        line = ser.readline()
        print(incoming_bytes, line, ser.in_waiting)

def _decrypt_message(ciphertext_bytes: bytes):
    plaintext_bytes = PRIVATE_KEY.decrypt(
        ciphertext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext_bytes

def _verify_sender(signature_bytes: bytes, plaintext_bytes: bytes):
    pass

def _verify_bytes(signature_bytes: bytes, plaintext_bytes: bytes, verification_key: RSAPublicKey):
        verification_key.verify(
        signature_bytes,
        plaintext_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

def _dict_to_bytes(payload_bytes: bytes):
    payload_dict = loads(payload_bytes.decode())

    ciphertext_str = payload_dict["ciphertext"]
    signature_str = payload_dict["signature"]

    ciphertext_bytes = ciphertext_str.encode("latin1")
    signature_bytes = signature_str.encode("latin1")
    return ciphertext_bytes, signature_bytes


if __name__ == "__main__":
    read_messages()

