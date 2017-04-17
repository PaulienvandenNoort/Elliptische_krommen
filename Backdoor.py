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
        elif self.x == other.x and self.y != other.y:
            return Punt() #twee punten die boven elkaar liggen (elkaars inverse) optellen geeft oneindig
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
        antwoord = self
        if n == 0:
            return 0
        if n == 1:
            return antwoord
        else:
            for i in range(n-1):
                antwoord += self
            return antwoord

    def binkeer(self,n): #bron https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Double-and-add
        if n == 0:
            return 0
        elif n == 1:
            return self
        elif n % 2 == 1:
            return self.optellen(self.binkeer(n-1))
        else:
            return (2*self).binkeer(n // 2)
        
    

        
def extended_euclidean_algorithm(a, b):
    """
    Returns a three-tuple (gcd, x, y) such that
    a * x + b * y == gcd, where gcd is the greatest
    common divisor of a and b.
    This function implements the extended Euclidean
    algorithm and runs in O(log b) in the worst case.    """
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = b, a
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_r, old_s, old_t
t
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



import random
import os

# Normale werking van de generator Dual_EC_DRBG is als volgt

def PRNG(n,d):
    Q = Punt(3,4,ElliptischeKromme(1,-1,104729))
    P = Q.binkeer(d)
    i0 = os.urandom(32)

    lijstinput = n*[0] #lijst van i'tjes in bytes
    lijstinput[0] = int.from_bytes(i0, byteorder='big')
    lijstoutput = (n-1)*[0] #lijst van o'tjes in bytes
    
    for i in range(1,n):
        #Byteorder moet nog ff checken
        
        lijstinput[i] = (P.binkeer(lijstinput[i-1])).x

    for i in range(n-1):
        phi = (Q.binkeer(lijstinput[i+1])).x
        #lijstoutput[i] = phi
        lijstoutput[i]= phi.to_bytes((phi.bit_length() + 7) // 8, byteorder='big')[-30:] #Hier moeten nog de eerste 2 bytes vanaf

    print(lijstoutput)
    return Q.binkeer(lijstinput[1])

    
def PRNG_backdoor(n=int(),d=int(),A=Punt()):
    
    Q = Punt(3,4,ElliptischeKromme(1,-1,104729))
    P = Q.binkeer(d)
    
    lijstinput = n*[0] #lijst van itjes in bytes
    lijstoutput = (n-1)*[0] #lijst van otjes in bytes

    i1P=A.binkeer(d)
    lijstinput[0] = 0
    lijstinput[1] = 0
    lijstinput[2] = i1P.x #integer
    #lijstoutput[0] = A.x
    lijstoutput[0] = (A.x).to_bytes(((A.x).bit_length() + 7) // 8, byteorder='big')

    for i in range(3,n):
        lijstinput[i] = (P.binkeer(lijstinput[i-1])).x

    for i in range(1,n-1):
        #lijstoutput[i] = (Q.binkeer(lijstinput[i+1])).x
        phi = (Q.binkeer(lijstinput[i+1])).x
        lijstoutput[i] = phi.to_bytes((phi.bit_length() + 7) // 8, byteorder='big')

    return lijstoutput
