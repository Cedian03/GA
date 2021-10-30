from cryptography.hazmat.primitives.asymmetric import rsa
from dataclasses import dataclass

@dataclass(unsafe_hash=True)
class Contact:
    """Class for storing contact data"""
    name: str
    information: str
    public_key: rsa.RSAPublicKey

