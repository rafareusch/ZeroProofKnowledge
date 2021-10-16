import sys
import collections

Coord = collections.namedtuple("Coord", ["x", "y"])

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

class  EC(object):

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
    
    def add(self, p1, p2, a, b, q): 
        """<add> of elliptic curve: negate of 3rd cross point of (p1,p2) line
        >>>  c = ec.add(a, b)
        >>> assert ec.is_valid(a)
        >>> assert ec.add(c, ec.neg(b)) == a
        """
        if p1 == self.zero: return p2
        if p2 == self.zero: return p1
        if p1.x == p2.x and p1.y != p2.y:
            # p1 + -p1 == 0
            return self.zero
        if p1.x == p2.x:
            # p1 + p1: use tangent line of p1 as (p1,p1) line
            l = (3 * p1.x * p1.x + self.a) * inv(2 * p1.y, self.q) % self.q
            pass
        else:
            l = (p2.y - p1.y) * inv(p2.x - p1.x, self.q) % self.q
            pass
        x = (l * l - p1.x - p2.x) % self.q
        y = (l * (p1.x - x) - p1.y) % self.q
        return Coord(x, y)


    if __name__ == "__main__":
        # y**2 = x**3 + A * x + B
        CurveA = 2
        CurveB = 2
        CurvePrime = 100
        Coord = 


        # enc/dec usage
        #ec = EC(1, 18, 19)
        #eg = ElGamal(ec)
        # priv = 5
        # pub1, _ = ec.at(7)
        # plain, _ = ec.at(1)
        
    