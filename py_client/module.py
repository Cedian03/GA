from base64 import decodebytes
from base64 import encodebytes

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

# load private key from file
PRIVATE_KEY = serialization.load_pem_private_key(
        open("self/private.pem", "rb").read(),
        password=None
    )

# # load private key from file
# def load_private_key(file_path: str):
#     return serialization.load_pem_private_key(
#         open(file_path, "rb").read(),
#         password=None
#     )

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
    cipher = encodebytes(cipher_bytes)
    return cipher

# decrypts bytes cipher to string 
def decrypt_message(cipher):
    cipher_bytes = decodebytes(cipher)
    plain_bytes = PRIVATE_KEY.decrypt(
        cipher_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    plain = plain_bytes.decode("utf-8")
    return plain
