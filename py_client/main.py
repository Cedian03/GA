import glob
import json
import os 
from tkinter import Tk
from dataclasses import dataclass

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from module import *

@dataclass(unsafe_hash=True)
class Contact:
    """Class for storing contact data"""
    name: str
    comment: str
    public_key: RSAPublicKey



# clear console 
def clear_console():
    return os.system("cls" if os.name in ("nt", "dos") else "clear")

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

# input() but preconfigured to send >>> and have check condition
def user_input(condition=()):
    if not condition: return input(">>> ")
    while True:
        inp = input(">>> ")
        if condition(inp):
            break
    return inp

def send_message():
    print("Please choose a contact to recive the message [0-{}]".format(len(CONTACTS) - 1))
    for index, contact in enumerate(CONTACTS):
        print(f"[{index}] {contact.name}: '{contact.comment}'") 

    def check(inp):
        return inp.isnumeric() and inp in [str(x) for x in range(len(CONTACTS))]

    inp = user_input(check)
    reciver = CONTACTS[int(inp)]

    print("Please enter your message to {}?".format(reciver.name))
    message = user_input()

    return encrypt_message(message, reciver.public_key)

# this would not be used with real nodes, this is for manual use of the system only 
def manual_send_message():
    message_bytes = send_message()
    message = message_bytes.decode("utf-8")

    r.clipboard_clear()
    r.clipboard_append(message)
    r.update() # now it stays on the clipboard after the window is closed
    print("Copied ciphertext to clipboard")

# 
def read_messages():
    pass

def manual_read_messages():
    cipher = r.clipboard_get()
    cipher_bytes = bytes(cipher, "utf-8")
    print(decrypt_message(cipher_bytes))

# send help
def cmd_help():
    for CMD in COMMANDS:
        print("{}\t{}".format(CMD, COMMANDS.get(CMD)[1]))



def main():
    try: # init
        print("Initialising...")

        print("Loading contacts...", end=" ")
        global CONTACTS 
        CONTACTS = load_contacts()
        print("OK")

        print("Loading commands...", end=" ")
        global COMMANDS
        COMMANDS = {"HELP":  (cmd_help, "This help list"),
                    "QUIT":  (quit, "Finito"), 
                    "SEND":  (send_message, "Send a message using connected node"),
                    "READ":  (read_messages, "Read messages from memory and connected node"),
                    "MSEND": (manual_send_message, "Manual use only"),
                    "MREAD": (manual_read_messages, "Manual use only")}
        print("OK")

        print("Setting up tkinter...", end=" ")
        global r 
        r = Tk()
        r.withdraw()
        print("OK")

    except Exception as e:
        print("ERROR\nAn error occured while initialising. ")
        print(e)
        quit()

    else:
        print("Initialising... OK")
        clear_console() # clear console after init
        # cmd_help() # start terminal with help list

    while True:
        inp = input(">>> ").upper()
        # try:
        COMMANDS.get(inp, lambda: print("Invalid command"))[0]()
        # except Exception as e:
        #     print("An error ocurred while executing command")
        #     print(e)

if __name__ == "__main__":
    main()

