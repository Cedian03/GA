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

# Choose two distinct prime numbers, p and q 
p = 61
q = 53 

# Compute n, such as n = pq 
n = p * q

# Compute the Carmichael's totient function of 
A = lcm(p, q)

e = 3