from dataclasses import dataclass
from json import loads
from serial import Serial
from time import sleep

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from util import decodecorator, load_contacts
from util import PRIVATE_KEY, READ_BYTE, SER_PORT, SER_BAUDRATE

# @dataclass
# class Message:
#     message: str
#     sender: Contact | None
#     reciver: Contact | None

@decodecorator()
def read_messages(*args, **kwargs):
    """read
    """
    with Serial(SER_PORT, SER_BAUDRATE, timeout=1) as ser:
        _read_init()
        
        # while ser.in_incoming:
        #     incoming_dict = ser.readLine()
        #     ciphertext_bytes, signature_bytes = _dict_to_bytes(incoming_dict)
        #     
        #     plaintext_bytes = _decrypt_bytes(ciphertext_bytes) # err if not for me
        #     sender_contact = _identify_sender(signature_bytes, plaintext_bytes)
        #     
        #     plaintext_str = plaintext_bytes.decode()
            
def _read_init():
    ser.write(READ_BYTE)
    sleep(3)

def _save_incoming_messages():
    pass

def _load_stored_messages():
    pass

def _decrypt_bytes(ciphertext_bytes: bytes):
    plaintext_bytes = PRIVATE_KEY.decrypt(
        ciphertext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext_bytes

def _identify_sender(signature_bytes: bytes, plaintext_bytes: bytes):
    contacts = load_contacts()
    
    for contact in contacts:
        if _verify_bytes(signature_bytes, plaintext_bytes, contact.public_key):
            return contact
    return None

def _verify_bytes(signature_bytes: bytes, plaintext_bytes: bytes, verification_key: RSAPublicKey):
    try:
        verification_key.verify(
            signature_bytes,
            plaintext_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    except: return False
    else: return True

def _dict_to_bytes(payload_bytes: bytes):
    payload_dict = loads(payload_bytes.decode())

    ciphertext_str = payload_dict["ciphertext"]
    signature_str = payload_dict["signature"]

    ciphertext_bytes = ciphertext_str.encode("latin1")
    signature_bytes = signature_str.encode("latin1")
    return ciphertext_bytes, signature_bytes


if __name__ == "__main__":
    read_messages()

