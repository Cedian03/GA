"""
"""

from os import listdir

from base64 import b64encode, b64decode

CONTACT_FOLDER = "./contacts"

def translate(m: int, key: tuple): 
    return pow(m, key[1], key[0]) 

def encrypt(M: str, key: tuple):
    m_bytes  = str.encode(M)                                                         # 
    m_number = int.from_bytes(m_bytes, "big")                                       # padding?

    c_number = translate(m_number, key)                                            #
    c_bytes  = c_number.to_bytes((c_number.bit_length() + 7) // 8, byteorder="big")  #
    c_text   = b64encode(c_bytes).decode()                                            #
    return c_text

def safe_encrypt(M: str, key1: tuple, key2: tuple):
    return encrypt(encrypt(M, key1), key2)

def decrypt(c: str, key: tuple):
    c_bytes  = b64decode(c)                                                          #                                                                        
    c_number = int.from_bytes(c_bytes, "big")                                       #        

    m_number = translate(c_number, key)                                            #
    m_bytes  = m_number.to_bytes((m_number.bit_length() + 7) // 8, byteorder="big")  #     
    m_text   = m_bytes.decode()                                               #
    return m_text                                  

def safe_decrypt(c: str, key1: tuple, key2: tuple):
    return decrypt(decrypt(c, key1), key2)

def get_key(folder: str, file: str):
    keys_str   = open("{}/{}/{}".format(CONTACT_FOLDER, folder, file)).read()
    keys_list  = keys_str.split(",")
    keys_tuple = 

    return 

def get_contacts():
    contacts = {}

    for folder in listdir(CONTACT_FOLDER):
        if folder == "_self":
            continue
        else:
            contacts[folder] = {}
            contacts[folder]["PUBLIC_KEY"] = tuple(open("{}/{}/public.key".format(CONTACT_FOLDER, folder)).read())
    
    return (PUBLIC_KEY, PRIVATE_KEY, contacts)

if __name__ == "__main__":
    PRIVATE_KEY = get_key("_self", "private.key")
    PUBLIC_KEY = get_key("_self", "public.key")

    print(c := encrypt("Hallo?", PRIVATE_KEY))