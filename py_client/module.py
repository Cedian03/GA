from base64 import decodebytes
from base64 import encodebytes

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

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
def encrypt_message(message_bytes: bytes, encryption_key: RSAPublicKey):
    cipher_bytes = encryption_key.encrypt(
        message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    signature_bytes = PRIVATE_KEY.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )    

    # bytes would be sent via serial to node
    # bytes are converted to b64 for readablity 
    cipher_base64 = encodebytes(cipher_bytes)
    signature_base64 = encodebytes(signature_bytes)
    return cipher_base64, signature_base64

# decrypts bytes cipher to string and bytes
def decrypt_message(cipher_base64: bytes):
    cipher_bytes = decodebytes(cipher_base64)
    plain_bytes = PRIVATE_KEY.decrypt(
        cipher_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plain_bytes

def sign_bytes(message: bytes):
    """Using private key"""
    signature_bytes = PRIVATE_KEY.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )    
    return signature_bytes


# verify bytes with public key, signature and plaintext
def verify_bytes(verification_key: RSAPublicKey, signature: bytes, plaintext: bytes):
    verification_key.verify(
        signature,
        plaintext,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )