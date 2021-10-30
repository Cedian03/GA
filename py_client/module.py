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

# 
def encrypt_message(message, encryption_key):
    message_bytes = bytes(message, "utf-8")
    ciphertext_bytes = encryption_key.encrypt(
        message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(ciphertext_bytes)