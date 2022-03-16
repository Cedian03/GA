# from base64 import decodebytes
# from base64 import encodebytes
from dataclasses import dataclass
import json

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey


DEBUG_MODE = True

SER_PORT = "COM3"
SER_BAUDRATE = 115200

SEND_BYTE = b"S"
READ_BYTE = b"R"
CONF_BYTE = b"C"

@dataclass
class Contact:
    name: str
    info: str
    public_key: RSAPublicKey | None

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

def success(*args, **kwargs):
    return console.print(*args, **kwargs, style="success")

def info(*args, **kwargs):
    return console.print(*args, **kwargs, style="info")

def debug(text): 
    if DEBUG_MODE: return console.print(f"Debug: {text}", style="debug")

def warning(*args, **kwargs):
    return console.print(*args, **kwargs, style="warning")

def danger(*args, **kwargs):
    return console.print(*args, **kwargs, style="danger")

def decodecorator(*kws):
    def decorator(fun):
        def wrapper(*args):
            if len(args) >= len(kws):
                if len(args) > len(kws): 
                    debug("too many args")
                kwargs = {}
                for idx, i in enumerate(kws):
                    kwargs[i] = args[idx]
                return fun(**kwargs)
            warning(f"Too few arguments provided, expected \"{kws}\"")
        return wrapper
    return decorator

def debugdeco(func):
    def wrapper(*args):
        debug(f"{func.__name__}{args}")
        try: 
            res = func(*args)
            debug(f"{func.__name__}{args} => {res}")
            return res
        except Exception as e:
            if DEBUG_MODE:
                debug(f"{func.__name__}{args} => {e}")
            return None
    return wrapper

# load private key from file
try: 
    PRIVATE_KEY = serialization.load_pem_private_key(
        open("self/private.pem", "rb").read(),
        password=None
    )
except:
    danger(f"No private key was found at \"self/private.pem\".\nConsider using X to generate one")

# loads any public key from file
@debugdeco
def load_public_key(file_name: str):
    try: 
        public_key = serialization.load_pem_public_key(
            open(f"contacts/{file_name.lower()}.pem", "rb").read()
        ) 
        return public_key  
    except: 
        warning(f"No public key found for \"{file_name}\"")
        return None
    
# 
@debugdeco
def load_contact(contact_name: str):    
    contacts = load_contacts()
    for contact in contacts:
        if contact.name.lower() == contact_name.lower():
            return contact
    return None

# 
@debugdeco
def load_contacts():
    with open("contacts.json", "rb") as f:
        contacts_data = json.load(f)

    contacts = []
    for contact in contacts_data:
        contacts.append(Contact(
            contact["name"],
            contact["info"],
            load_public_key(contact["name"])
        ))
    return contacts

#
@debugdeco
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


if __name__ == "__main__":
    print(load_contacts())
    print(parse("send \"Hej Charlie\" Charlie"))
    success("This is success.")
    info("This is info.")
    debug("This is debug.")
    warning("This is warning.")
    danger("This is danger.")

