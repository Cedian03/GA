"""
"""

from os import listdir

from base64 import b64encode, b64decode

CONTACT_FOLDER = "./contacts"

def translate(m: int, n: int, p: int): 
    return pow(m, p, n) 

def encrypt(M: str, n: int, p: int):
    print(M)
    m_bytes = str.encode(M)                 
    print(m_bytes)                                        # 
    m_number = int.from_bytes(m_bytes, "big") 
    print(m_number)

    c_number = translate(m_number, n, p)                                            #
    print(c_number)
    c_bytes = c_number.to_bytes((c_number.bit_length() + 7) // 8, byteorder="big")  #
    print(c_bytes)
    c_text = b64encode(c_bytes).decode() 
    print(c_text)                                           #
    return c_text

def safe_encrypt(M: str, n1: int, p1: int, n2: int, p2: int):
    c = encrypt(M, n1, p1)
    print("~~~")
    c2 = encrypt(c, n2, p2)
    return c2

def decrypt(c: str, n: int, p: int):
    print(c)
    c_bytes = b64decode(c)                                                          #     
    print(c_bytes)                                                                   
    c_number = int.from_bytes(c_bytes, "big")                                       #    
    print(c_number)    

    m_number = translate(c_number, n, p)                                            #
    print(m_number)
    m_bytes = m_number.to_bytes((m_number.bit_length() + 7) // 8, byteorder="big")  #  
    print(m_bytes)   
    m_text = m_bytes.decode() 
    print(m_text)
    return m_text                                  

def safe_decrypt(c: str, n1: int, p1: int, n2: int, p2: int):
    c2 = decrypt(c, n1, p1)
    print("~~~")
    m = decrypt(c2, n2, p2)
    return m

def get_key(folder: str, file: str):
    return tuple(open("{}/{}/{}".format(CONTACT_FOLDER, folder, file)).read().split(","))

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

    n = 308347617367612890077
    d = 91828655823170799323
    e = 65537

    other_n = 2728993228477849637033
    other_d = 499571448214113729893
    other_e = 65537

    # n = 155686150820030975386173570295803749152016571796242749928954290106635424475963428330856860718451300609
    # d = 364268365955230352504037649372869141071128387541401994331295580680801936496619605807590240599911873
    # e = 65537

    # other_n = 277995974867813928690953481596235319839742245874847459901965819385253636977266595579813374312384410681
    # other_d = 105619127763265528135868230389023930700972916843319966572674924674659282791723026724225184210642799575
    # other_e = 65537

    M = "x"

    print("\n")
    c = encrypt(M, n, d)
    print("~~~")
    c2 = encrypt(c, other_n, other_e)
    print("~~~~~")
    m = decrypt(c2, n, e)
    print("~~~")
    m2 = decrypt(m, other_n, other_d)
    print("\n")
    
    # print("\n")
    # c = safe_encrypt(M, n, d, other_n, other_e)
    # print("~~~~~")
    # m = safe_decrypt(c, other_n, other_d, n, e)
    # print("\n")
