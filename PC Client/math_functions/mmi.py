"""Modular multiplicative inverse

Link: https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
"""

def mmi_naive(a: int, m: int):
    for x in range(m):
        if (a * x) % m == 1:
            return x

def mmi_iterative(a: int, m: int):
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
