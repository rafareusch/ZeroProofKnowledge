import sys
from collections import namedtuple


Point = namedtuple("Point", "x y")

# The point at infinity (origin for the group law).
O = 'Origin'

# Given curve
# y**2 = x**3 + A * x + B (2,2)

p = 17 # random prime (?)
a = 2
b = 2


def inv(n, q):
    """div on PN modulo a/b mod q as a * inv(b, q) mod q
    >>> assert n * inv(n, q) % q == 1
    """
    for i in range(q):
        if (n * i) % q == 1:
            return i
        pass
    assert False, "unreached"
    pass


def sqrt(n, q):
    """sqrt on PN modulo: it may not exist
    >>> assert (sqrt(n, q) ** 2) % q == n
    """
    assert n < q
    for i in range(1, q):
        if i * i % q == n:
            return (i, q - i)
        pass
    raise Exception("not found")


def valid(P):
    """
    Determine whether we have a valid representation of a point
    on our curve.  We assume that the x and y coordinates
    are always reduced modulo p, so that we can compare
    two points for equality with a simple ==.
    """
    if P == O:
        return True
    else:
        return (
            (P.y**2 - (P.x**3 + a*P.x + b)) % p == 0 and
            0 <= P.x < p and 0 <= P.y < p)

def inv_mod_p(x):
    """
    Compute an inverse for x modulo p, assuming that x
    is not divisible by p.
    """
    if x % p == 0:
        raise ZeroDivisionError("Impossible inverse")
    return pow(x, p-2, p)

def ec_inv(P):
    """
    Inverse of the point P on the elliptic curve y^2 = x^3 + ax + b.
    """
    if P == O:
        return P
    return Point(P.x, (-P.y)%p)

def ec_add(P, Q):
    """
    Sum of the points P and Q on the elliptic curve y^2 = x^3 + ax + b.
    """
    if not (valid(P) and valid(Q)):
        raise ValueError("Invalid inputs")

    # Deal with the special cases where either P, Q, or P + Q is
    # the origin.
    if P == O:
        result = Q
    elif Q == O:
        result = P
    elif Q == ec_inv(P):
        result = O
    else:
        # Cases not involving the origin.
        if P == Q:
            dydx = (3 * P.x**2 + a) * inv_mod_p(2 * P.y)
        else:
            dydx = (Q.y - P.y) * inv_mod_p(Q.x - P.x)
        x = (dydx**2 - P.x - Q.x) % p
        y = (dydx * (P.x - x) - P.y) % p
        result = Point(x, y)

    # The above computations *should* have given us another point
    # on the curve.
    assert valid(result)
    return result


if __name__ == "__main__":
    P = Point(5, 1)
    Q = Point(5, 1)
    #R = Point(2, 3103)
    TwoP = ec_add(P, P)
    print(TwoP)
    # ThreeP = ec_add(TwoP, P)
    # Compute 4P two different ways.
    #assert ec_add(P, ThreeP) == ec_add(TwoP, TwoP)
    # Check the associative law.
    #assert ec_add(P, ec_add(Q, R)) == ec_add(ec_add(P, Q), R)

 
    priv = 5
    # pub1, _ = ec.at(7)
    # plain, _ = ec.at(1)