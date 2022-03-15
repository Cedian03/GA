from send import send_message
from read import read_messages
from contacts import add_contact, list_contacts, remove_contact
from util import parse, warning

COMMANDS = {
    "send": send_message,
    "read": read_messages,
    "list": list_contacts,
    "cadd": add_contact,
    "crmv": remove_contact
}

def help(*args):
    pass

def loop():
    while True:
        inp = input("> ")
        par = parse(inp)
        cmd = par.pop(0)

        if cmd.lower() in COMMANDS.keys():
            COMMANDS[cmd](*par)
        else:
            warning("That command was not found. Use X to see all commands.")
        

if __name__ == "__main__":
    loop()

    
