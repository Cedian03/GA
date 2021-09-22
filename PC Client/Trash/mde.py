"""Modular exponentiation

https://en.wikipedia.org/wiki/Modular_exponentiation
"""
def mde(x: int, n: int, mod: int):
    """function modular_pow(base, exponent, modulus) is
    if modulus = 1 then
        return 0
    c := 1
    for e_prime = 0 to exponent-1 do
        c := (c * base) mod modulus
    return c
    """
    if mod == 1:
        return 0
    c = 1
    for e_prime in range(n):
        c = (c * x) % mod
    return c