"""Rivest–Shamir–Adleman

"""

def translate(m: int, n: int, p: int): 
    return pow(m, p, n) 

def str_to_int(M: str):
    return int("".join([format(ord(i), "08b").zfill(8) for i in M]), 2)

def int_to_str(c: int):
    bi_string = "{0:b}".format(c)
    if len(bi_string) % 8:
        bi_string = bi_string.zfill(len(bi_string) + (8 - len(bi_string) % 8))
    int_list = [int(bi_string[8 * i:8 * (i + 1)], 2) for i in range(len(bi_string) // 8)]
    
    return "".join([chr(i) for i in int_list])

def main():
    t = True if input("en/de: ") == "en" else False
    M = input("M: ")

    n = int(input("n: ")) 
    p = int(input("p: ")) 

    if t:
        print("Encrypting...")
        m = str_to_int(M)
        c = translate(m, n, p)
        print(c)
    else:
        print("Decrypting...")
        M = translate(int(M), n, p)
        m0 = int_to_str(M)
        print(m0)

if __name__ == "__main__":
    main()
