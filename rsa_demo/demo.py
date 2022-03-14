# Implemented from Wikipedia 
# https://en.wikipedia.org/wiki/RSA_(cryptosystem)

from numpy import mod


def gcd(a: int, b: int):
    """## Greatest common divisor\n
       https://en.wikipedia.org/wiki/Greatest_common_divisor
    """
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def lcm(a: int, b: int):
    """## Least common multiple\n
       https://en.wikipedia.org/wiki/Least_common_multiple
    """
    return (a * b) // gcd(a, b)

# def ctf(a: int, b: int):
#     """## Carmichael's totient function\n
#        \"Since n = pq, λ(n) = lcm(λ(p), λ(q)), and since p and q are prime, λ(p) = φ(p) = p - 1, and likewise λ(q) = q - 1. Hence λ(n) = lcm(p - 1, q - 1)\"\n
#        https://en.wikipedia.org/wiki/Carmichael_function
#     """
#     return lcm(a - 1, b - 1)

def mmi(a: int, m: int):
    """## Modular multiplicative inverse\n
       This method only if a and m are coprime\n
       https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
    """
    m0, y, x = m, 0, 1

    if m == 1:
        return 0

    while a > 1:
        q = a // m
        t = m
        
        m = a % m
        a = t
        t = y

        y = x - q * y 
        x = t

    if x < 0:
        x = x + m0
    
    return x

# Key generation

# Choose two distinct prime numbers, such as
p = 61
q = 53 

# Choose two distinct prime numbers, such as
n = p * q # => 3233

# Compute the Carmichael's totient function of the product as λ(n) = lcm(p − 1, q − 1) giving
λ = lcm(p - 1, q - 1) # => 780 

# Choose any number 1 < e < 780 that is coprime to 780. Choosing a prime number for e leaves us only to check that e is not a divisor of 780
e = 17 

# Compute d, the modular multiplicative inverse of e (mod λ(n)), yielding
d = mmi(e, λ) # => 413

# (n, e) forms the public key 
# (n, d) forms the private key 

# Encryption

# The public key is (n = 3233, e = 17). For a padded plaintext message m, the encryption function is
m = 65 # <= The message
c = mod(m**e, n)

# The private key is (n = 3233, d = 413). For an encrypted ciphertext c, the decryption function is
m2 = mod(c**d, n)

print(f"m: {m} => c: {c} => m2: {m2}") # => "m: 65 => c: 2790 => m2: 65"

