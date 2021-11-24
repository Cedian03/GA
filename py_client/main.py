import glob
from inspect import signature
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

# copy to clipboard
def copy(text: str):
    r.clipboard_clear()
    r.clipboard_append(text)
    r.update() # now it stays on the clipboard after the window is closed

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

# send message 
def send_message():
    print("Please choose a contact to recive the message [0-{}]".format(len(CONTACTS) - 1))
    for index, contact in enumerate(CONTACTS):
        print("[{}] {}: '{}'".format(index, contact.name, contact.comment)) 

    def check(inp):
        return inp.isnumeric() and inp in [str(x) for x in range(len(CONTACTS))]

    inp = user_input(check)
    reciver = CONTACTS[int(inp)]

    print("Please enter your message to {}?".format(reciver.name))
    message = user_input()
    message_bytes = bytes(message, "utf-8")

    return encrypt_message(message_bytes, reciver.public_key)

# for manual use of the system
def manual_send_message():
    message_bytes, signature_bytes = send_message()
    message = message_bytes.decode("utf-8")
    signature = signature_bytes.decode("utf-8")

    verify_bytes(PRIVATE_KEY.public_key(), signature_bytes, message_bytes)

    copy(message)
    print("Copied ciphertext to clipboard")

    print("Continue to copy signature")
    input("...")
    copy(signature)
    print("Copied signature to clipboard")

# read stored messages
def read_messages():
    pass

# for manual use of the system
def manual_read_messages():
    cipher = r.clipboard_get()
    cipher_bytes = bytes(cipher, "utf-8")
    plain_bytes = decrypt_message(cipher_bytes)
    print(plain_bytes.decode("utf-8"))

    print("Please copy message signature (or don't)")
    input("...\r")

    signature = r.clipboard_get()
    signature_bytes = bytes(signature, "utf-8")

    print(signature_bytes)

    for contact in CONTACTS:
        try: 
            verify_bytes(contact.public_key, signature_bytes, plain_bytes)
        except:
            print("Failed to verify {} as author".format(contact.name))
        else:
            print("Message author verifed as {}".format(contact.name))
            break
    else:
        print("Message author could not me verified")

# help command
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
        try:
            COMMANDS.get(inp, lambda: print("Invalid command"))[0]()
        except Exception as e:
            print("An error ocurred while executing command")
            print(e)

if __name__ == "__main__":
    main()

