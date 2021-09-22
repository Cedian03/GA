"""Lowest common multiple
"""

from gcd import gcd_recursive as gcd

def lcm(a: int, b: int):
    return (a * b) // gcd(a, b)