import copy

class Montgomery_curve:
    """ definieert een Montgomery kromme,
    curve25519 is hier een speciaal geval van"""

    def __init__(self,b,a,p):
        self.a = a
        self.b = b
        self.p = p

    def __str__(self):
        if self.b*(self.a**2-4)!=0:
            return 'E: ' + str(self.b) + 'y^2 = x^3 + ' + str(self.a) + 'x^2 + x'
        else:
            return 'Kan niet'

    def __eq__(self,other):
        return self.a == other.a and self.b == other.b and self.p == other.p

class Punt_op_Montgomery_curve:
    """ definieert de berekeningen die gedaan kunnen worden met Montgomery krommen,
    deze verschillen vooral in de optelling van de berekeningen van de
    elliptische kromme zoals in het basisdeel gedefinieerd """

    def __init__(self,x=[],y=[],c=Montgomery_curve(0,0,2)):
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

        # twee punten die boven elkaar liggen optellen geeft oneindig:
        elif self.x == other.x and self.y != other.y:
            return Punt()
        # raaklijn recht omhoog voor punt bij zichzelf optellen geeft oneindig:
        elif self == other and self.y == 0:
            return Punt()

        # afleiding van onderstaande formules staat in het verslag:
        else:
            if self == other:
                s = (3*self.x**2+2*self.a*self.x+1)*inverse_of(2*self.b*self.y,self.p)
                xr = (self.b*s**2 - self.a - 2*self.x) % self.p
                yr = (self.y + (xr - self.x)*(3*self.x**2 + 2*self.a*self.x + 1)*inverse_of(2*self.b*self.y,self.p)) % self.p

                antwoord = -Punt(xr,yr,self.E)
                 
            else:
                s = (other.y - self.y)* inverse_of((other.x - self.x),self.p)
                xr = (self.b*s**2 - self.a - self.x - other.x) % self.p
                yr = ((2*self.x+other.x+self.a)*s - self.b*s**3 - self.y) % self.p

                antwoord = Punt(xr,yr,self.E) #de negatie is hier al meegenomen

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

# We kunnen nu met curve25519 rekenen door onderstaand commando aan te roepen:
curve25519 = Montgomery_curve(1,486662,2**(255)-19)

