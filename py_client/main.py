import glob
import json
import os 
from dataclasses import dataclass

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa

os.chdir(r"C:\Users\Algot\Documents\GA\py_client")

@dataclass(unsafe_hash=True)
class Contact:
    """Class for storing contact data"""
    name: str
    comment: str
    public_key: rsa.RSAPublicKey

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

# def debug(log_info):
#     def decorator(func):
#         def wrapper(*args):
#             if LOG_TOGGLE:
#                 print(log_info + "...", end=" ")
#                 try: 
#                     result = func(*args)
#                 except:
#                     print("ERROR")
#                 else:
#                     print("OK")
#             else:
#                 result = func(*args)

#             return result
#         return wrapper
#     return decorator

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
    return contacts

def recive_input(condition):
    while True:
        inp = input(">>> ")
        if condition(inp):
            break
    return inp

def send_message():
    print(f"Please choose a contact to recive the message [0-{len(CONTACTS) - 1}]")
    for index, contact in enumerate(CONTACTS):
        print(f"[{index}] {contact.name}: '{contact.comment}'") 

    def check(inp):
        return inp.isnumeric() and inp in [str(x) for x in range(len(CONTACTS))]

    inp = recive_input(check)

    print(inp)

def read_messages():
    pass

def h():
    print("no help")

def main():
    try: # init
        print("Initialising...")

        print("Loading contacts...", end=" ")
        global CONTACTS 
        CONTACTS = load_contacts()
        print("OK")

        print("Loading private key...", end=" ")
        global PRIVATE_KEY 
        PRIVATE_KEY = load_private_key("self/private.pem")
        print("OK")

    except:
        print("\nAn error occured while Initialising. ")
        quit()

    else:
        print("Initialising... OK")
        clearConsole() # Clear console after init

    cmd =  {"help": h,
            "send": send_message,
            "read": read_messages}

    while True:
        inp = input(">>> ").lower()
        if inp == "quit": 
            clearConsole()
            quit()
        try:
            cmd.get(inp, lambda: print("Invalid command"))()
        except:
            print("An error ocurred while executing command")

if __name__ == "__main__":
    main()