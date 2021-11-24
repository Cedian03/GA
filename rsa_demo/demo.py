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

def clf(a: int, b: int):
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

# Choose two distinct prime numbers, p and q 
p = 61
q = 53 

# Compute n, such as n = pq 
n = p * q

# Compute the Carmichael's lambda function of p and q to 
A = clf(p, q) # A used instead of lambda

e = 17

d = mmi(e, A)

print(d)