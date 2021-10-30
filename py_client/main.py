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

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

clearConsole()

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

# load contacts from contacts folder 
def load_contacts():
    contacts = []
    for filename in glob.iglob("contacts/*.json"):
        with open(filename, "rb") as f:
            contact = json.load(f)
            contacts.append(
                Contact(
                    contact["name"], 
                    contact["comment"], 
                    load_public_key("contacts/" + contact["public_key"])))


def main():
    try: # init
        print("Starting")

        print("Loading keys")
        global CONTACTS 
        CONTACTS = load_contacts()

        print("Loading contacts")
        global PRIVATE_KEY 
        PRIVATE_KEY = load_private_key("self/private.pem")

    except:
        print("An error occured on start. ")
        quit()

    while True:
        input(">>> ")

    print("Closing...")
    quit()

if __name__ == "__main__":
    main()