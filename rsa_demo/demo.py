# Implemented from Wikipedia 

def gcd(a: int, b: int):
    """
    """
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def lcm(a: int, b: int):
    """
    """
    return (a * b) // gcd(a, b)

def ctf(a: int, b: int):
    """
    """
    return lcm(a - 1, b - 1)

def mmi(a: int, m: int):
    """a and m are coprime
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

# Choose two distinct prime numbers, such as
p = 61
q = 53 

# Compute n = pq giving
n = p * q # => 3233

# Compute the Carmichael's totient function of the product as ctf(n) = lcm(p − 1, q − 1) giving 
x = ctf(p, q) # => 780 # x used to represent the variable

# Choose any number 1 < e < 780 that is coprime to 780. Choosing a prime number for e leaves us only to check that e is not a divisor of 780.
e = 17

# Compute d, the modular multiplicative inverse of e (mod λ(n)) yielding,
d = mmi(e, x) # => 413

print(d)