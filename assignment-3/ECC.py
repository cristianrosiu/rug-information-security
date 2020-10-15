# Expresses number 1 as the difference between multiples
# of a and b using euclidean gcd
def egcd(a, b):
    if a == 0:
        return 0, 1
    else:
        y, x = egcd(b % a, a)
        return x - (b // a) * y, y


# Returns the modulo inverse of 2 numbers
def modulo_inverse(n, m):
    x, y = egcd(n, m)
    return x % m


# Point class in order to ease our work
class EllipticPoint:
    # Initialize X and Y
    def __init__(self, X, Y, a, p):
        self.X = X
        self.Y = Y
        self.a = a
        self.p = p

    # Checks if 2 points are equal
    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y

    # Returns a copy of current point
    def copy(self):
        return EllipticPoint(self.X, self.Y, self.a, self.p)

    def __repr__(self):
        return 'EllipticPoint()'

    # Displays the point
    def __str__(self):
        return "(%d, %d)" % (self.X, self.Y)

    # Returns -Point
    def __neg__(self):
        return EllipticPoint(self.X, -self.Y, self.a, self.p)

    # Adding 2 points (P and Q) in the group.
    # First step is to draw the line(slope) through P and Q -> will yield -Result (and we need to find Result)
    # To compute Result = P+Q we just compute the reflection of -Result
    def __add__(self, other):
        if isinstance(other, Identity):
            return self
        if self == other:
            # If slope goes to infinity, return the Identity of the group.
            if self.Y == 0:
                return Identity(0)
            # Computes the tangent to the elliptical curve of the given point.
            slope = ((3 * self.X * self.X + self.a) * modulo_inverse((2 * self.Y), p)) % p
        else:
            if self.X == other.X:
                return Identity(0)
            # Computes the slope of 2 points. Because we can't normally divide in modulo group we used modulo_inverse
            # function instead of the normal division sign '/'
            slope = ((other.Y - self.Y) * modulo_inverse((other.X + p - self.X), p)) % p
        # Calculate the Result point.
        new_x = (slope * slope - self.X - other.X) % p
        new_y = (slope * (self.X - new_x) - self.Y) % p

        return EllipticPoint(new_x, new_y, self.a, self.p)

    def __sub__(self, other):
        return self + -other

    # Uses the Double and Add method (similar to binary).
    def __mul__(self, n):
        P = self
        R = Identity(0)

        while n:
            if n % 2 == 1:
                R = R + P
            P = P + P
            n = n // 2

        return R

    def __rmul__(self, n):
        return self * n


# Class which contains the logic of the Identity element.
# P + Identity = P
# P * Identity = Identity
class Identity(EllipticPoint):
    def __init__(self, Y):
        self.Y = Y

    def __neg__(self):
        return self

    def __str__(self):
        return "Identity"

    def __add__(self, other):
        return other

    def __mul__(self, n):
        return self

    def __eq__(self, other):
        return type(other) is Identity


if __name__ == '__main__':
    # Get the input
    x, y = [int(x) for x in input().strip(' ()\r').split(',')]
    a, b, p = [int(x) for x in input().split(' ')]
    m, n = [int(x) for x in input().split(' ')]
    generator = EllipticPoint(x, y, a, p)

    bob = n * generator
    print(m * bob)
