import glob
import json
import os 
from dataclasses import dataclass

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from module import *

@dataclass(unsafe_hash=True)
class Contact:
    """Class for storing contact data"""
    name: str
    comment: str
    public_key: rsa.RSAPublicKey

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

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

def user_input(condition=()):
    if not condition: return input(">>> ")
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

    inp = user_input(check)
    reciver = CONTACTS[int(inp)]

    print(f"What do you want to send to {reciver.name}?")
    message = user_input()

    print(encrypt_message(message, reciver.public_key))

# this would not be used with real nodes, this is for manual use of the system only 
def dec_message():
    print("Please")
    inp = user_input()
    print(inp)
    print(bytes(inp[:-1], "utf-8"))

def h():
    print("no help")

def main():
    try: # init
        print("Initialising...")

        print("Loading contacts...", end=" ")
        global CONTACTS 
        CONTACTS = load_contacts()
        print("OK")

    except Exception as e:
        print("\nAn error occured while initialising. ")
        print(e)
        quit()

    else:
        print("Initialising... OK")
        clearConsole() # Clear console after init

    cmd =  {"help": h,
            "send": send_message,
            "manual": dec_message}

    while True:
        inp = input(">>> ").lower()
        if inp == "quit": 
            clearConsole()
            quit()
        # try:
        cmd.get(inp, lambda: print("Invalid command"))()
        # except Exception as e:
        #     print("An error ocurred while executing command")
        #     print(e)

if __name__ == "__main__":
    main()

