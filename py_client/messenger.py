# Message handling
# 

# contacts too?

import serial

# cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey


from main import Contact

class Messenger(): # Message encoding, decoding, encryption and decryption and serial 
    def __init__(self, private_key: RSAPrivateKey):
        self.private_key = private_key 
        self.public_key = self.private_key.public_key()

        self.port = "COM3"
        self.baudrate = 9600

    def send(self, message_str: str, contact: Contact):
        message_bytes = message_str.encode()
        encryption_key = contact.public_key
        
        ciphertext_bytes = self._encrypt_bytes(message_bytes, encryption_key)
        # signature_bytes = self._sign_bytes(message_bytes)



    def read(self):
        pass

    def _encrypt_bytes(self, message_bytes: bytes, encryption_key: RSAPublicKey):
        ciphertext_bytes = encryption_key.encrypt(
            message_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return ciphertext_bytes

    def _sign_bytes(self, message_bytes: bytes):
        signature_bytes = self.private_key.sign(
            message_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return signature_bytes
    
    def _serial_write(self, payload_bytes: bytes):
        with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
            if ser.out_waiting():
                print("Serial out not empty when sending")

            ser.write(payload_bytes)

