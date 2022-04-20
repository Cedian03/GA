from json import dumps
from time import sleep

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from serial import Serial

from util import (PRIVATE_KEY, SEND_BYTE, SER_BAUDRATE, SER_PORT, debug,
                  debugdeco, decodecorator, load_contact)
         
# @decodecorator("message_str", "contact_name")
def send_message(*args, **kwargs):
    """send <message_str> <contact_name>
    """
    ser = kwargs["ser"]

    message_str = args[0]
    contact_name = args[1]

    contact = load_contact(contact_name)
    
    message_bytes  = message_str.encode()
    encryption_key = contact.public_key
    
    ciphertext_bytes = encrypt_bytes(message_bytes, encryption_key)
    signature_bytes  = sign_bytes(message_bytes)

    payload_bytes = bytes_to_dict(ciphertext_bytes, signature_bytes)
    serial_write(ser, payload_bytes)

@debugdeco
def encrypt_bytes(message_bytes: bytes, encryption_key: RSAPublicKey):
    ciphertext_bytes = encryption_key.encrypt(
        message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext_bytes

@debugdeco
def sign_bytes(message_bytes: bytes):
    signature_bytes = PRIVATE_KEY.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature_bytes

@debugdeco
def bytes_to_dict(ciphertext_bytes: bytes, signature_bytes: bytes):
    ciphertext_str = ciphertext_bytes.decode("latin1")
    signature_str = signature_bytes.decode("latin1")

    payload_dict = {
        "ciphertext": ciphertext_str,
        "signature": signature_str
    }

    payload_bytes = dumps(payload_dict).encode()
    return payload_bytes

@debugdeco
def serial_write(ser: Serial, payload_bytes: bytes):
    if ser.out_waiting:
        debug("Serial out not empty when sending")

    # ser.flushInput()
    # ser.flushOutput()
    ser.write(payload_bytes)

