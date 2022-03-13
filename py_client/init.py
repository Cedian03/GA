# # global imports/functions/variables/classes

# import json

# from serial import Serial

# #rich: https://rich.readthedocs.io/en/latest/index.html
# from rich.console import Console
# from rich.theme import Theme
# custom_theme = Theme({
#     "info": "dim cyan",
#     "warning": "magenta",
#     "danger": "bold red"
# })

# console = Console(theme=custom_theme)

# def info(*args):
#     return console.print(args, style="info")

# def warning(*args):
#     return console.print(args, style="warning")

# def danger(*args):
#     return console.print(*args, style="danger")

# # def input():
#     # pass

# from dataclasses import dataclass

# # cryptography: 
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.primitives.asymmetric import padding
# from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
# from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

# @dataclass
# class Contact:
#     name: str
#     info: str
#     public_key: RSAPublicKey

# # load private key from file
# PRIVATE_KEY = serialization.load_pem_private_key(
#         open("self/private.pem", "rb").read(),
#         password=None
#     )

# port = "COM3"
# baudrate = 115200