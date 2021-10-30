import glob
import json
import os 
from dataclasses import dataclass

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

os.chdir(r"C:\Users\Algot\Documents\GA\py_client")

@dataclass(unsafe_hash=True)
class Contact:
    """Class for storing contact data"""
    name: str
    comment: str
    public_key: rsa.RSAPublicKey

# load public key from file
def load_public_key(file_path):
    return serialization.load_pem_public_key(
        open(file_path, "rb").read()
    )

# load contacts from contacts folder 
def load_contacts():
    contacts = []
    for filename in glob.iglob("contacts/*.json"):
        with open(filename, "rb") as f:
            contact = json.load(f)
            contacts.append(Contact(contact["name"], contact["comment"], load_public_key("contacts/" + contact["public_key"])))

def main():
    load_contacts()

if __name__ == "__main__":
    main()