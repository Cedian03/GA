"""
"""

from random import choice
import sys

sys.path.insert(1, "./math_functions")

from clf import clf_cheat as clf
from gcd import gcd_recursive as gcd
from mmi import mmi_iterative as mmi
from psw import baillie_psw as psw

def generate_prime(digits):
    while True:
        if digits == 0:
            return 0

        p = 0
        li_digits = [n for n in range(10)]
        for i in range(digits - 1):
            p += choice(li_digits) * 10**(i + 1)
        p += (choice(li_digits) * 2) % 10 + 1

        if psw(p):
            return p

def main(s):
    p, q = generate_prime(s), generate_prime(s + 10)
    n = p * q
    An = clf(p, q)
    e = 2**16 + 1
    if gcd(e, An) != 1 or e < An:
        ValueError()
    d = mmi(e, An)

    print(n.bit_length())

    return "modulus (n): {}, \nprivate expo (d): {}, \npublic expo (e): {}".format(n, d, e)

if __name__ == "__main__":
    print(main(200))
