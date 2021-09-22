"""Greatest common divisor 

Wikipeda article: https://en.wikipedia.org/wiki/Greatest_common_divisor
"""

def gcd_division(a: int, b: int): 
    """Division based implementation using the Euclidean algorithm
    """
    while b != 0:
        t = b
        b = a % b
        a = t
    return a

def gcd_recursive(a: int, b:int):
    """Recursive implementation using the Euclidean algorithm
    """
    if b == 0:
        return a
    else:
        return gcd_recursive(b, a % b)
