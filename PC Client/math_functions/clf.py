from gcd import gcd_recursive as gcd
from lcm import lcm 

def clf(n: int):
    """Carmichael lambda function

    https://en.wikipedia.org/wiki/Carmichael_function
    """
    coprimes = [x for x in range(1, n) if gcd(x, n) == 1]
    k = 1 
    while not all(pow(x, k, n) == 1 for x in coprimes):
        k += 1
    return k

def clf_cheat(p: int, q: int):
    """
    """
    return lcm(p - 1, q - 1)