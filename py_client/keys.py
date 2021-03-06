# from os.path import isfile

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def key_generation():
    # heads up if private and/or public key already exist
    # if isfile("self/private.pem") or isfile("self/public.pem"):
    #     print("Private key and/or public key already exists. Are you sure you want to generate a new key pair (this will override old keys) [y/N]")
    #     if input(">>> ").lower() != "y":
    #         raise Exception

    # Source https://gist.github.com/ostinelli/aeebf4643b7a531c248a353cee8b9461

    # Save file helper  
    def save_file(filename, content):  
        f = open("self/{}".format(filename), "wb")  
        f.write(content) 
        f.close()  
    
    # Generate private key & write to disk  
    private_key = rsa.generate_private_key(  
        public_exponent=65537,  
        key_size=2048,  
        backend=default_backend()  
    )  
    pem = private_key.private_bytes(  
        encoding=serialization.Encoding.PEM,  
        format=serialization.PrivateFormat.PKCS8,  
        encryption_algorithm=serialization.NoEncryption()  
    )  
    save_file("private.pem", pem)  
    
    # Generate public key  
    public_key = private_key.public_key()  
    pem = public_key.public_bytes(  
        encoding=serialization.Encoding.PEM,  
        format=serialization.PublicFormat.SubjectPublicKeyInfo  
    )  
    save_file("public.pem", pem)  

if __name__ == "__main__":
    key_generation()

