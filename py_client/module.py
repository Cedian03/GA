from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

# load private key from file
def load_private_key(file_path):
    return serialization.load_pem_private_key(
        open(file_path, "rb").read(),
        password=None
    )

# load public key from file
def load_public_key(file_path):
    return serialization.load_pem_public_key(
        open(file_path, "rb").read()
    )

