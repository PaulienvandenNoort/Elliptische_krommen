import math
import copy

class ElliptischeKromme:
    """Definieert een elliptische kromme van de vorm y^2 = x^3 + ax + b en vraagt het
    priemgetal van het lichaam waarop de kromme gedefinieerd is."""

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
    """Definieert een punt op de kromme door de x en y coördinaat van het punt en de 
    bijbehorende elliptische kromme te vragen. Verder worden de berekeningen die 
    gedaan kunnen worden met elliptische krommen hieronder gedefinieerd."""
    
    def __init__(self,x=[],y=[],c=ElliptischeKromme(0,0,2)):
        self.x = x
        self.y = y
        self.E = c
        self.a = c.a
        self.b = c.b
        self.p = c.p
        
    #voer het punt oneindig in als Punt()

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
        
        # punt bij oneindig optellen geeft punt zelf:
        if self.x==[] and self.y==[]:
            return other
        elif other.x==[] and other.y==[]:
            return self
        
        elif self.E != other.E:
            return 'Kan niet'
        
        #twee punten die boven elkaar liggen (elkaars inverse) optellen geeft oneindig:
        elif self.x == other.x and self.y != other.y:
            return Punt()
        #raaklijn recht omhoog voor punt bij zichzelf optellen geeft oneindig:
        elif self == other and self.y == 0:
            return Punt()
        
        # afleiding van onderstaande formules staat in het verslag:
        else:
            if self == other:
                s = (3*self.x**2+self.a)* inverse_of(2*self.y,self.p)
            else:
                s = (self.y - other.y)* inverse_of((self.x - other.x),self.p)

            xr = (s**2 - self.x - other.x) % self.p
            yr = (self.y+s*(xr-self.x)) % self.p        

            antwoord = -Punt(xr,yr,self.E)

            return antwoord

    def negatie(self):
        new = copy.deepcopy(self)
        new.y = -new.y % self.p
        return new

    def vermenigvuldigen(self,n):
        antwoord = self
        if n == 0:
            return 0
        if n == 1:
            return antwoord
        else:
            for i in range(n-1):
                antwoord += self
            
            return antwoord

        
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

def BruteForce(p=Punt(),q=Punt()):
    n = p.p
    for i in range(1,n):
        pnext = p.vermenigvuldigen(i)
        if pnext==q:
            return 'q = '+str(i)+' keer p'
