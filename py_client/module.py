from base64 import decodebytes
from base64 import encodebytes

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

# load private key from file
def load_private_key(file_path: str):
    return serialization.load_pem_private_key(
        open(file_path, "rb").read(),
        password=None
    )

# load public key from file
def load_public_key(file_path: str):
    return serialization.load_pem_public_key(
        open(file_path, "rb").read()
    )

# encrypt string message to bytes 
def encrypt_message(message, encryption_key):
    message_bytes = bytes(message, "utf-8")
    cipher_bytes = encryption_key.encrypt(
        message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    # bytes would be sent via serial to node
    # bytes are converted to b64 for readablity 
    cipher_base64 = encodebytes(cipher_bytes)
    print(cipher_base64)
    