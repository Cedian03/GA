import json

from util import Contact, debugger, success, info, warning, danger
from util import load_contact


@debugger
def add_contact(*args):
    """add contact_name contact_info"""
    contact_name = args[0]
    contact_info = args[1]

    if load_contact(contact_name):
        warning(f"A contact with the name \"{contact_name}\" already exist.")
        return

    with open("contacts.json", "rb") as f:
        contacts = json.load(f)
    
    contacts.append({
        "name": contact_name,
        "info": contact_info
    })

    with open("contacts.json", "w") as f:
        json.dump(contacts, f, indent=4)
    
    success(f"Successfully added contact \"{contact_name}: {contact_info}\".")
    info(f"You will need to manually add \"{contact_name}\"'s public key at \"contacts/{contact_name.lower()}.pem\" if not done already.")

@debugger
def remove_contact(*args):
    """remove contact_name"""
    contact_name = args[0]

    if not load_contact(contact_name):
        warning(f"No contact with the name \"{contact_name}\" could be found.")
        return

    with open("contacts.json", "rb") as f:
        contacts = json.load(f)
    
    for contact in contacts:
        if contact["name"].lower() == contact_name.lower():
            contacts.remove(contact)
            success(f"Successfully removed contact \"{contact_name}\".")
            info(f"You will need to manually remove \"{contact_name}\"'s public key at \"contacts/{contact_name.lower()}.pem\" if not done already.")
            break

    with open("contacts.json", "w") as f:
        json.dump(contacts, f, indent=4)

@debugger
def list_contacts(*args):
    """list *search"""
    print(bool(args))
    if args:
        search = args[0]
    else:
        search = ""

    print(type(search))

    with open("contacts.json", "rb") as f:
        contacts = json.load(f)

    for i in contacts:
        contact_name = i["name"]
        contact_info = i["info"]
        
        if contact_name.lower().startswith(search.lower()): 
            info(f"{contact_name}\t: {contact_info}")


if __name__ == "__main__":
    list_contacts("Alg")
    add_contact("Isak", "Snel hest")

