import json

from util import Contact, decodecorator, load_contacts, success, info, warning, danger
from util import load_contact


@decodecorator("contact_name", "contact_info")
def add_contact(**kwargs):
    """add <contact_name> <contact_info>
    """
    contact_name = kwargs["contact_name"]
    contact_info = kwargs["contact_info"]

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
    
    # success(f"Successfully added contact \"{contact_name}: {contact_info}\".")
    # info(f"You will need to manually add \"{contact_name}\"'s public key at \"contacts/{contact_name.lower()}.pem\" if not done already.")

@decodecorator("contact_name")
def remove_contact(**kwargs):
    """remove <contact_name>
    """
    contact_name = kwargs["contact_name"]

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

@decodecorator()
def list_contacts(**kwargs):
    """list 
    """
    contacts = load_contacts()
    
    for contact in contacts:
        info(f"{contact.name}\t: ", end="")
        if contact.public_key:
            info(contact.info)
        else:
            warning("No public key avalible")

if __name__ == "__main__":
    list_contacts()
