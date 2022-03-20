from dataclasses import dataclass
from json import dump, load, loads
from time import sleep

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from serial import Serial

from util import (PRIVATE_KEY, READ_BYTE, SER_BAUDRATE, SER_PORT, Contact,
                  decodecorator, load_contacts)


@dataclass
class Message:
    message: str
    sender: Contact | None

@decodecorator("limit")
def read_messages(*args, **kwargs):
    """read <?limit>
    """

    limit = int(kwargs["limit"])

    with Serial(SER_PORT, SER_BAUDRATE, timeout=1) as ser:
        _read_init(ser)
        
        _save_incoming_messages(ser)
        messages = _load_stored_messages()
        
        _display_messages(messages, limit)
            
def _read_init(ser: Serial):
    ser.write(READ_BYTE)
    sleep(3)

def _save_incoming_messages(ser: Serial):
    messages = _load_stored_messages()
    while ser.in_incoming:
        payload_dict = ser.readLine()
        ciphertext_bytes, signature_bytes = _dict_to_bytes(payload_dict)
        
        plaintext_bytes = _decrypt_bytes(ciphertext_bytes) # err 
        sender_contact = _identify_sender(signature_bytes, plaintext_bytes)
        
        plaintext_str = plaintext_bytes.decode()
        
        messages.append(Message(
            plaintext_str,
            sender_contact
        ))
        
    with open("history.json", "w") as f:
        dump(messages, f)

def _load_stored_messages():
    with open("history.json", "r") as f:
        messages = load(f)
    return messages

def _display_messages(messages: list[Message], limit: int):
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

def _dict_to_bytes(payload_dict: bytes):
    payload_dict = loads(payload_dict.decode())

    ciphertext_str = payload_dict["ciphertext"]
    signature_str = payload_dict["signature"]

    ciphertext_bytes = ciphertext_str.encode("latin1")
    signature_bytes = signature_str.encode("latin1")
    return ciphertext_bytes, signature_bytes


if __name__ == "__main__":
    read_messages()

