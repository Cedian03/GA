# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.primitives.asymmetric import padding

# message = b"ok?"

# # load private key from file
# private_key = serialization.load_pem_private_key(
#         open("self/private.pem", "rb").read(),
#         password=None
#     )

# public_key = private_key.public_key()

# ciphertext = public_key.encrypt(
#         b"message",
#         padding.OAEP(
#             mgf=padding.MGF1(algorithm=hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None
#         )
#     )

# signature = private_key.sign(
#     message,
#     padding.PSS(
#         mgf=padding.MGF1(hashes.SHA256()),
#         salt_length=padding.PSS.MAX_LENGTH
#     ),
#     hashes.SHA256()
# )

# public_key.verify(
#     signature,
#     message,
#     padding.PSS(
#         mgf=padding.MGF1(hashes.SHA256()),
#         salt_length=padding.PSS.MAX_LENGTH
#     ),
#     hashes.SHA256()
# )

# print(signature)

# import serial
# ser = serial.Serial('COM3', 9600, timeout=1)  # open serial port
# print(ser.name)         # check which port was really used
# ser.write(b'hello')     # write a string
# ser.close()             # close port

# import serial
# import time

# with serial.Serial("COM3", 9600, timeout=1) as ser:
#     while True:
#         i = input("in:").encode()
#         if i == "done":
#             break
#         ser.write(i)
#         time.sleep(.5)
#         r = ser.read_all()
#         # s = r.decode().replace("\r\n", "")
#         print(r)
#         print(i == r)

# foo = "send 'Godmorgon Charlie' Charlie"

# def parse(s):
#     def egg(x):
#         if x != "":
#             r.append(x.strip())
            
#     r = []
#     w = ""
#     c = False
#     for i in s:
#         if i == "'":
#             egg(w)
#             w = ""
#             c = not c
#         elif i == " " and not c:
#             egg(w)
#             w = ""
#         else:
#             w += i

#     if c: # Err?
#         pass

#     egg(w)

#     return r

# print(parse(foo))

