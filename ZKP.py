import sys
import numpy as np
from collections import namedtuple


Point = namedtuple("Point", "x y")

# The point at infinity (origin for the group law).
O = 'Origin'

# Given curve
# y**2 = x**3 + A * x + B (2,2)

#p = 2111
#a = 20
#b = 13
p = 17 # random prime (?)
a = 2
b = 2


#https://crypto.stackexchange.com/questions/11743/scalar-multiplication-on-elliptic-curves/74710


# Extended Euclidean algorithm
def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m


def ecc_double(P):
    x1,y1 = P
    s = ((3*(x1**2) + a) * modinv(2*y1, p))%p
    x3 = (s**2 - x1 - x1)%p
    y3 = (s*(x1-x3) - y1)%p
    return Point(x3, y3)


def ecc_add(P1, P2):
    s = 0
    x1,y1 = P1
    x2,y2 = P2
    if (x1==x2):
        s = ((3*(x1**2) + a) * modinv(2*y1, p))%p
    else:
        s = ((y2-y1) * modinv(x2-x1, p))%p
    x3 = (s**2 - x1 - x2)%p
    y3 = (s*(x1 - x3) - y1)%p
    return Point(x3, y3)

def double_and_add(multi, P):
    (x3, y3)=(0, 0)
    (x1, y1) = (P.x, P.y)
    (x_tmp, y_tmp) = (P.x, P.y)
    init = 0
    for i in str(bin(multi)[2:]):
        if (i=='1') and (init==0):
            init = 1
        elif (i=='1') and (init==1):
            (x3,y3) = ecc_double(Point(x_tmp, y_tmp))
            (x3,y3) = ecc_add(Point(x1,y1), Point(x3, y3))
            (x_tmp, y_tmp) = (x3, y3)
        else:
            (x3, y3) = ecc_double(Point(x_tmp, y_tmp))
            (x_tmp, y_tmp) = (x3, y3)
    result  = Point(x3, y3)
    return result



if __name__ == "__main__":
    P = Point(5, 1)
    Q = Point(5, 1)

    result = ecc_add(Q,P)
    print(result)
    
    result = double_and_add(11, P)
    print(result)

