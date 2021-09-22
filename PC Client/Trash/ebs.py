"""Exponentiation by squaring

Wikipedia article: https://en.wikipedia.org/wiki/Exponentiation_by_squaring
"""

def ebs(x: int, n: int):
    """
    """
    if n <= 0:
        raise ValueError()

    if n == 0:
        return 1
    elif n == 1:
        return x
    elif (n % 2) == 0:
        return ebs(x**2, n//2)
    else:
        return x * ebs(x**2, (n - 1)//2)

def ebs_iterative(x: int, n: int): 
    """Function exp_by_squaring_iterative(x, n)
    if n < 0 then
      x := 1 / x;
      n := -n;
    if n = 0 then return 1
    y := 1;
    while n > 1 do
      if n is even then 
        x := x * x;
        n := n / 2;
      else
        y := x * y;
        x := x * x;
        n := (n – 1) / 2;
    return x * y
    """ 
    if n < 0:
        x = 1 / x
        n = -n
    if n == 0:
        return 1
    y = 1
    while n > 1:
        if n % 2 == 0:
            x *= x
            n /= 2
        else:
            y *= x
            x *= x
            n = (n - 1) / 2
    return x * y