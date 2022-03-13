# from base64 import decodebytes
# from base64 import encodebytes
from dataclasses import dataclass
import json

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

@dataclass
class Contact:
    name: str
    info: str
    public_key: RSAPublicKey

#rich: https://rich.readthedocs.io/en/latest/index.html
from rich.console import Console
from rich.theme import Theme
custom_theme = Theme({
    "success": "bold green",
    "info": "bold white",
    "debug": "bold cyan",
    "warning": "bold yellow",
    "danger": "bold red"
})

console = Console(theme=custom_theme)

def success(text):
    return console.print(text, style="success")

def info(text):
    return console.print(text, style="info")

def debug(text): 
    if debug_mode: return console.print(f"Debug: {text}", style="debug")

def warning(text):
    return console.print(text, style="warning")

def danger(text):
    return console.print(text, style="danger")

# Decorator/wrapper for 
def debugger(func):
    def wrapper(*args, **kwargs):
        try: 
            debug(f"{func.__name__}{args, kwargs}")
            return func(*args, **kwargs)
        except Exception as e:
            danger("There was an Error executing that command.")
            print(e)

    return wrapper

# load private key from file
try: 
    f = open("self/private.pem", "rb").read()
    PRIVATE_KEY = serialization.load_pem_private_key(f, password=None)
except:
    danger(f"No private key was found at \"self/private.pem\".\nConsider using X to generate one")


# loads any public key from file
def load_public_key(file_name: str):
    try: 
        f = open(f"contacts/{file_name.lower()}.pem", "rb").read()
        return serialization.load_pem_public_key(f)   
    except: 
        danger(f"No public key was found at \"contacts/{file_name}.pem\".")
        exit()
    
# 
def load_contact(contact_name: str):    
    with open("contacts.json", "rb") as f:
        contacts = json.load(f)

    for contact in contacts:
        if contact["name"].lower() == contact_name.lower():
            try:
                return Contact(contact["name"], 
                       contact["info"], 
                       load_public_key(contact["name"]))
            except:
                return

def list_contacts():
    with open("contacts.json", "rb") as f:
        contacts = json.load(f)

    contact_names = []
    for i in contacts:
        contact_names.append(i["name"])

    return contact_names

def parse(inp: str):
    def egg(x):
        if x != "":
            out.append(x.strip())
 
    out = []
    seg = ""
    quo = False
    for char in inp:
        if char in ("'", "\""):
            egg(seg)
            seg = ""
            quo = not quo
        elif char == " " and not quo:
            egg(seg)
            seg = ""
        else:
            seg += char

    if quo: # Err?
        pass

    egg(seg)

    return out

debug_mode = True

ser_port = "COM3"
ser_baudrate = 115200

if __name__ == "__main__":
    print(list_contacts())
    print(parse("send \"Hej Charlie\" Charlie"))
    success("This is success.")
    info("This is info.")
    debug("This is debug.")
    warning("This is warning.")
    danger("This is danger.")

# # encrypt string message to bytes 
# def encrypt_message(message_bytes: bytes, encryption_key: RSAPublicKey):
#     cipher_bytes = encryption_key.encrypt(
#         message_bytes,
#         padding.OAEP(
#             mgf=padding.MGF1(algorithm=hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None
#         )
#     )

#     signature_bytes = PRIVATE_KEY.sign(
#         message_bytes,
#         padding.PSS(
#             mgf=padding.MGF1(hashes.SHA256()),
#             salt_length=padding.PSS.MAX_LENGTH
#         ),
#         hashes.SHA256()
#     )    

#     # bytes would be sent via serial to node
#     # bytes are converted to b64 for readablity 

#     cipher_base64 = encodebytes(cipher_bytes)
#     signature_base64 = encodebytes(signature_bytes)
#     return cipher_base64, signature_base64

# # decrypts bytes cipher to string and bytes
# def decrypt_message(cipher_base64: bytes):
#     cipher_bytes = decodebytes(cipher_base64)
#     plain_bytes = PRIVATE_KEY.decrypt(
#         cipher_bytes,
#         padding.OAEP(
#             mgf=padding.MGF1(algorithm=hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None
#         )
#     )
#     return plain_bytes

# def sign_bytes(message: bytes):
#     """Using private key"""
#     signature_bytes = PRIVATE_KEY.sign(
#         message,
#         padding.PSS(
#             mgf=padding.MGF1(hashes.SHA256()),
#             salt_length=padding.PSS.MAX_LENGTH
#         ),
#         hashes.SHA256()
#     )    
#     return signature_bytes


# # verify bytes with public key, signature and message
# def verify_bytes(verification_key: RSAPublicKey, signature: bytes, message: bytes):
#         verification_key.verify(
#         signature,
#         message,
#         padding.PSS(
#             mgf=padding.MGF1(hashes.SHA256()),
#             salt_length=padding.PSS.MAX_LENGTH
#         ),
#         hashes.SHA256()
#     )