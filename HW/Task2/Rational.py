import sys


def gcd(fst, snd):
    ''' Returns gcd of 2 numbers
    '''
    while snd:
        fst, snd = snd, fst % snd
    return fst


class Rational:
    ''' rational number implementation m in Z; n in N
    '''

    def divide_on_gcd(self):
        our_gcd = gcd(int(self.numerator), int(self.denominator))
        self.numerator /= our_gcd
        self.denominator /= our_gcd
        return self

    def __init__(self, numerator=0, denominator=1):
        self.numerator = numerator
        self.denominator = denominator
        self.divide_on_gcd()

    # unary

    def __neg__(self):
        return Rational(-self.numerator, self.denominator)

    def __str__(self):
        return str(int(self.numerator)) + '/' + str(int(self.denominator))

    # binary functions

    def __eq__(self, other):
        return (self.numerator == other.numerator) and (self.denominator == other.denominator)

    def __ne__(self, other):
        return not (self == other)

    def __add__(self, other):
        return Rational(self.numerator * other.denominator + self.denominator * other.numerator,
                        self.denominator * other.denominator).divide_on_gcd()

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        return Rational(self.numerator * other.numerator,
                        self.denominator * other.denominator).divide_on_gcd()

    def __truediv__(self, other):
        return Rational(self.numerator * other.denominator,
                        self.denominator * other.numerator).divide_on_gcd()

exec(sys.stdin.read())
