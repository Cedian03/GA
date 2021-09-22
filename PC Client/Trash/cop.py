"""
"""

from gcd import gcd_recursive as gcd

def cop(n: int):
    return [x for x in range(n) if gcd(x, n) == 1]

def cop_half(n: int):
    x = n // 3
    while x < n:
        if gcd(x, n) == 1:
            return x
        x += 1

# print(cop(100))