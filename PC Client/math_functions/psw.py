"""Baillie-PSW probabilistic primality test

Stolen from: https://github.com/smllmn/baillie-psw
"""

from math import sqrt

def miller_rabin_base_2(n):
    """Perform the Miller Rabin primality test base 2"""
    d = n-1
    s = 0
    while not d & 1: # Check for divisibility by 2
        d = d >> 1 # Divide by 2 using a binary right shift
        s += 1

    x = pow(2, d, n)
    if x == 1 or x == n-1:
        return True
    for i in range(s-1):
        x = pow(x, 2, n)
        if x == 1:
            return False
        elif x == n - 1:
            return True
    return False

def U_V_subscript(k, n, U, V, P, Q, D):
    k, n, U, V, P, Q, D = map(int, (k, n, U, V, P, Q, D))
    digits = list(map(int, str(bin(k))[2:]))
    subscript = 1
    for digit in digits[1:]:
        U, V = U*V % n, (pow(V, 2, n) - 2*pow(Q, subscript, n)) % n
        subscript *= 2
        if digit == 1:
            if not (P*U + V) & 1:
                if not (D*U + P*V) & 1:
                    U, V = (P*U + V) >> 1, (D*U + P*V) >> 1
                else:
                    U, V = (P*U + V) >> 1, (D*U + P*V + n) >> 1
            elif not (D*U + P*V) & 1:
                U, V = (P*U + V + n) >> 1, (D*U + P*V) >> 1
            else:
                U, V = (P*U + V + n) >> 1, (D*U + P*V + n) >> 1
            subscript += 1
            U, V = U % n, V % n
    return U, V

def lucas_pp(n, D, P, Q):                                                                                                                                                                                                                         
    """Perform the Lucas probable prime test"""
    U, V = U_V_subscript(n+1, n, 1, P, P, Q, D)

    if U != 0:
        return False

    d = n + 1
    s = 0
    while not d & 1:
        d = d >> 1
        s += 1

    U, V = U_V_subscript(n+1, n, 1, P, P, Q, D)

    if U == 0:
        return True

    for r in xrange(s):
        U, V = (U*V) % n, (pow(V, 2, n) - 2*pow(Q, d*(2**r), n)) % n
        if V == 0:
            return True

    return False

def jacobi_symbol(a, n):
    """Calculate the Jacobi symbol (a/n)"""
    if n == 1:
        return 1
    elif a == 0:
        return 0
    elif a == 1:
        return 1
    elif a == 2:
        if n % 8 in [3, 5]:
            return -1
        elif n % 8 in [1, 7]:
            return 1
    elif a < 0:
        return (-1)**((n-1)/2) * jacobi_symbol(-1*a, n)

    if a % 2 == 0:
        return jacobi_symbol(2, n) * jacobi_symbol(a / 2, n)
    elif a % n != a:
        return jacobi_symbol(a % n, n)
    else:
        if a % 4 == n % 4 == 3:
            return -1 * jacobi_symbol(n, a)
        else:
            return jacobi_symbol(n, a)
def D_chooser(candidate):
    """Choose a D value suitable for the Baillie-PSW test"""
    D = 5
    while jacobi_symbol(D, candidate) != -1:
        D += 2 if D > 0 else -2
        D *= -1
    return D

def baillie_psw(candidate):
    """Perform the Baillie-PSW probabilistic primality test on candidate"""

    # Check divisibility by a short list of primes less than 50
    for known_prime in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
        if candidate == known_prime:
            return True
        elif candidate % known_prime == 0:
            return False

    # Now perform the Miller-Rabin primality test base 2
    if not miller_rabin_base_2(candidate):
        return False
    
    # Check that the number isn't a square number, as this will throw out 
    # calculating the correct value of D later on (and means we have a
    # composite number)
    # the slight ugliness is from having to deal with floating point numbers
    if int(sqrt(candidate) + 0.5) ** 2 == candidate:
        return False

    # Finally perform the Lucas primality test
    D = D_chooser(candidate)
    if not lucas_pp(candidate, D, 1, (1-D)/4):
        return False

    # You've probably got a prime!
    return True

if __name__ == "__main__":
    print(baillie_psw(3))