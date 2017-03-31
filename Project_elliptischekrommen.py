import math
import copy

class ElliptischeKromme:

    def __init__(self,a,b,p):
        self.a = a
        self.b = b
        self.p = p

    def __str__(self):
        if -16*(4*self.a**3+27*self.b**2)!=0:
            return 'E: y^2 = x^3 + ' + str(self.a) + 'x + ' + str(self.b)
        else:
            return 'Kan niet'

    def __eq__(self,other):
        return self.a == other.a and self.b == other.b and self.p == other.p
            

class Punt:

    def __init__(self,x=[],y=[],c=ElliptischeKromme(0,0,2)):
        self.x = x #voer het punt oneindig in als Punt()
        self.y = y
        self.E = c
        self.a = c.a
        self.b = c.b
        self.p = c.p

    def __str__(self):
        if self.x==[] and self.y==[]:
            return 'O'
        return '(' + str(self.x) + ',' + str(self.y)+ ')'

    def __add__(self,other):
        return self.optellen(other)

    def __sub__(self,other):
        return self.optellen(other.negatie())

    def __neg__(self):
        return self.negatie()

    def __mul__(self,n):
        return self.vermenigvuldigen(n)

    def __rmul__(self,n):
        return self.vermenigvuldigen(n)

    def __eq__(self,other):
        return self.x==other.x and self.y==other.y and self.E==other.E

    def optellen(self,other):
        if self.x==[] and self.y==[]:
            return other
        elif other.x==[] and other.y==[]:
            return self #punt bij oneindig optellen geeft punt zelf
        
        elif self.E != other.E:
            return 'Kan niet'
        
        elif other == inverse_of(self, p):
            return Punt() #punt bij zn inverse optellen geeft oneindig
        elif self.x == other.x and self.y != other.y:
            return Punt() #twee punten die boven elkaar liggen optellen geeft oneindig
        elif self == other and self.y == 0:
            return Punt() #raaklijn recht omhoog voor punt bij zichzelf optellen geeft oneindig

        else:
            
            if self == other:
                s = (3*self.x**2+self.a)* inverse_of(2*self.y,self.p) #afgeleide van de elliptische kromme
            else:
                s = (self.y - other.y)* inverse_of((self.x - other.x),self.p)  #rc van de lijn door de twee punten

            xr = (s**2 - self.x - other.x) % self.p #afleiding in mn notities
            yr = (self.y+s*(xr-self.x)) % self.p #rc*x-afstand tussen p en r+punt p         

            antwoord = -Punt(xr,yr,self.E)

            return antwoord

    def negatie(self):
        new = copy.deepcopy(self)
        new.y = -new.y % self.p
        return new

    def vermenigvuldigen(self,n):
        if self.E != other.E:
            return 'Kan niet'
        else:
            antwoord = self
            if n == 0:
                return 0
            if n == 1:
                return antwoord
            else:
                for i in range(n-1):
                    antwoord += self
            
            return antwoord

    
#rc = (other.y - self.y)/(other.x - self.x)
        #bp = self.y - rc * self.x    
    
def extended_euclidean_algorithm(a, b):
    """
    Returns a three-tuple (gcd, x, y) such that
    a * x + b * y == gcd, where gcd is the greatest
    common divisor of a and b.

    This function implements the extended Euclidean
    algorithm and runs in O(log b) in the worst case.
    """
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = b, a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def inverse_of(n, p):
    """
    Returns the multiplicative inverse of
    n modulo p.

    This function returns an integer m such that
    (n * m) % p == 1.
    """
    gcd, x, y = extended_euclidean_algorithm(n, p)
    assert (n * x + p * y) % p == gcd

    if gcd != 1:
        # Either n is 0, or p is not a prime number.
        raise ValueError(
            '{} has no multiplicative inverse '
            'modulo {}'.format(n, p))
    else:
        return x % p

