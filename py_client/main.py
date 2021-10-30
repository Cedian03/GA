import glob
import json
import os 
from dataclasses import dataclass

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from debug import debug

os.chdir(r"C:\Users\Algot\Documents\GA\py_client")

@dataclass(unsafe_hash=True)
class Contact:
    """Class for storing contact data"""
    name: str
    comment: str
    public_key: rsa.RSAPublicKey

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

# load private key from file
@debug("Loading private key")
def load_private_key(file_path):
    return serialization.load_pem_private_key(
        open(file_path, "rb").read(),
        password=None
    )

# load public key from file
@debug("Loading public key")
def load_public_key(file_path):
    return serialization.load_pem_public_key(
        open(file_path, "rb").read()
    )

# load contacts from contacts folder 
@debug("Loading contacts")
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
        print("Initialising")

        global CONTACTS 
        CONTACTS = load_contacts()

        print("Loading contacts...", end=" ")
        global PRIVATE_KEY 
        PRIVATE_KEY = load_private_key("self/private.pem")
        print("OK")

    except:
        print("An error occured on start. ")
        quit()

    # clearConsole() # Clear console after init

    while True:
        input(">>> ")

    print("Closing...")
    quit()

if __name__ == "__main__":
    main()