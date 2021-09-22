from base64 import encodebytes
from base64 import decodebytes
from os import listdir

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

CONTACT_PATH = "./c"
PRIVATE_PATH = "./private.pem"

# Load private key from file
def load_private_key(file_path):
    return serialization.load_pem_private_key(
        open(file_path, "rb").read(),
        password=None
    )

# Load public key from file
def load_public_key(file_path):
    return serialization.load_pem_public_key(
        open(file_path, "rb").read()
    )

# Load contact (name, key) from contact folder ./c
def load_contacts_list():
    file_names = listdir(CONTACT_PATH)
    return [(f[:-4], load_public_key("{}/{}".format(CONTACT_PATH, f))) for f in file_names]

def encrypt_bytes(key, message: bytes):
    """Using public key"""
    ciphertext = key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def sign_bytes(message: bytes):
    """Using private key"""
    signature = PRIVATE_KEY.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )    
    return signature

def encrypt_message(reciver_key, message: str):
    message_bytes = bytes(message, "utf-8")
    ciphertext_bytes = encrypt_bytes(reciver_key, message_bytes)
    ciphertext_base64 = encodebytes(ciphertext_bytes)

    signature_bytes = sign_bytes(message_bytes)
    signature_base64 = encodebytes(signature_bytes)
    return ciphertext_base64, signature_base64

def decrypt_bytes(ciphertext: bytes) -> bytes:
    """Using private key"""
    plaintext = PRIVATE_KEY.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext

def verify_bytes(key, signature: bytes, plaintext: bytes):
    """Using public key"""
    try:
        key.verify(
            signature,
            plaintext,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    except:
        return False
    else:
        return True

def decrypt_message(sender_key, ciphertext: bytes, signature: bytes):
    ciphertext_bytes = decodebytes(ciphertext)
    plaintext_bytes = decrypt_bytes(ciphertext_bytes)
    plaintext = plaintext_bytes.decode("utf-8")

    signature_bytes = decodebytes(signature)
    verified = verify_bytes(sender_key, signature_bytes, plaintext_bytes)
    return plaintext, verified

def decode_message(contacts: list, ciphertext: bytes, signature: bytes):
    for contact in contacts:
        try:
            plaintext, v = decrypt_message(contact[1], ciphertext, signature)
        except:
            continue
        else:
            return plaintext, contacts v
    return "", None, False

if __name__ == "__main__":
    contacts = load_contacts_list()

    c = b"yuHAfmA0vqK0AShgX25SyZed+nfcgPEIUEJm2di69FvbR7gB6Zhjxof27cwBb6CWrHNWGsVFbR7Jc/+Jx1EcegA+BSdF4S3LDr+/QYtfgCPgxu9XF7N8uT9UlYLciR86GvFFPjvBdXz4nGtgauHyzFg73XgWYWcVL3+EghrWJ/n3Ngh7i86w1uo5cWKP1PpuBWt7tCrGbHYoAx9ggfiOGRA05CumhKcDURugvJnpLXy7rXHkHfpi1pWhlxL/mLx5yW72MdQBIKLvn2N/oZT6ptT/WwK1hNKVltCmCR+NLNSXEoM2Hvb3Rw6+dCZUKPEhcN6E3BWXgpnm/NY/MTCExQ=="
    s = b"fO6S9P+QBLSI2owq7u5ZtGaU3seDXIxlUBLZJPlzFgz/bUZ/5b+JHgAWvcuaUv5RY4ljQcAIvb6JSdG8fnkGwZCCq7aiU0ojMMFAruXxRhoNd+teA+RytK8V9kaiouqafZOhj3aqay9c8HlGaSqxpxlvRxgwpXdto1RCbWRHVZsYNO3/s29zlMaWJRp3zbQ1qpyPCMpZZwOIAD1JsR1Sl5fbl+T8jedHRTSOnlkpH7RySZ04fldSD6ZszJVC0H4Vntz93msmrPSan2HhVZBY043eOQuOJQXzVkQVDH4muYD/nJpjw5ScRN1SP2cR76DzsQPlKUpl6V5VaIyaXD6KVA=="

    def strip(s):
        return s.replace('\n', ' ').replace('\r', '').replace(" ", "")
    
    PRIVATE_KEY = load_private_key(PRIVATE_PATH)
    PUBLIC_KEY = PRIVATE_KEY.public_key()

    while True:
        if input("\n[E]ncryption / [D]ecryption: \n>>> ").lower() == "e":
            message = input("Message: \n>>> ")
            ciphertext, signature = encrypt_message(contacts[0][1], message)
            ciphertext, signature = ciphertext.decode(), signature.decode()
            print("\nCiphertext: \n{} \n\nSignature: \n{} ".format(strip(ciphertext), strip(signature)))
        else:
            ciphertext = bytes(input("Ciphertext: \n>>> "), "utf-8")
            signature = bytes(input("Signature: \n>>> "), "utf-8")
            plaintext, verified = decode_message(contacts, ciphertext, signature)
            print("\nPlaintext: \n{} \n\nSender Verified as {}: \n{} ".format(plaintext, CONVO_KEY, verified))


    print(decode_message(contacts, c, s))

    # while True:
    #     if input("\n[E]ncryption / [D]ecryption: \n>>> ").lower() == "e":
    #         message = input("Message: \n>>> ")
    #         ciphertext, signature = encrypt_message(CONVO_KEY, message)
    #         ciphertext, signature = ciphertext.decode(), signature.decode()
    #         print("\nCiphertext: \n{} \n\nSignature: \n{} ".format(strip(ciphertext), strip(signature)))
            
    #     else:
    #         ciphertext = bytes(input("Ciphertext: \n>>> "), "utf-8")
    #         signature = bytes(input("Signature: \n>>> "), "utf-8")
    #         plaintext, verified = decrypt_message(CONVO_KEY, ciphertext, signature)
    #         print("\nPlaintext: \n{} \n\nSender Verified as {}: \n{} ".format(plaintext, CONVO_KEY, verified))

