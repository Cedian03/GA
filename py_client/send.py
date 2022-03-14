from json import dumps
from serial import Serial
from time import sleep

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from util import debug, debugger
from util import load_contact
from util import SER_PORT
from util import SER_BAUDRATE
from util import PRIVATE_KEY
from util import SEND_BYTE


@debugger
def send_message(*args):
    """send message contact"""

    message_str = args[0]
    contact_name = args[1]

    contact = load_contact(contact_name)
    
    message_bytes  = message_str.encode()
    encryption_key = contact.public_key
    
    ciphertext_bytes = _encrypt_bytes(message_bytes, encryption_key)
    signature_bytes  = _sign_bytes(message_bytes)

    payload_bytes = _bytes_to_dict(ciphertext_bytes, signature_bytes)
    _serial_write(payload_bytes)

def _encrypt_bytes(message_bytes: bytes, encryption_key: RSAPublicKey):
    ciphertext_bytes = encryption_key.encrypt(
        message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return ciphertext_bytes

def _sign_bytes(message_bytes: bytes):
    signature_bytes = PRIVATE_KEY.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature_bytes

def _bytes_to_dict(ciphertext_bytes: bytes, signature_bytes: bytes):
    ciphertext_str = ciphertext_bytes.decode("latin1")
    signature_str = signature_bytes.decode("latin1")

    payload_dict = {
        "ciphertext": ciphertext_str,
        "signature": signature_str
    }

    payload_bytes = dumps(payload_dict).encode()

    return payload_bytes


def _serial_write(payload_bytes: bytes):
    with Serial(SER_PORT, SER_BAUDRATE, timeout=1) as ser:
        if ser.out_waiting:
            debug("Serial out not empty when sending")

        ser.write(SEND_BYTE + payload_bytes)

        # read
        sleep(3)
        while ser.in_waiting:
            print(ser.readline())


if __name__ == "__main__":
    send_message("Hej Charlie", "Charlie")

