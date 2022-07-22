import os, sys
import random
from hashlib import sha256
from re_microcrypt.utils.num_sublib import ext_randint, mod_inverse
class Curve():
    def __init__(self, p, a, b ,G, n):
        self.p = p
        self.a = a
        self.b = b
        self.G = G
        self.n = n

btcCurve = Curve(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F, 0, 7, (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8), 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141)

class Point():
    def __init__(self, x, y, curve:Curve):
        self.x = x
        self.y = y
        self.curve = curve
    
    def __add__(self, pnt2):
        if pnt2 is None:
            return self
        if self is None:
            return pnt2
        if self.x == pnt2.x:
            s:int = (3*self.x*self.x+self.curve.a)*mod_inverse(2*self.y, self.curve.p)
        else:
            s:int = (self.y - pnt2.y)*mod_inverse(self.x - pnt2.x, self.curve.p)
        x = (s**2 - self.x - pnt2.x) % self.curve.p
        y = -(self.y + s*(x - self.x)) % self.curve.p
        return Point(x, y, self.curve)

    def __str__(self):
        return f"x:{self.x}, y:{self.y}"
            
    def double(self):
        return self.__add__(self)
        
    def __mul__(self, oth):
        point = None
        subPoint = self
        while oth > 0:
            if oth & 1:
                point = subPoint + point
            subPoint = subPoint.double()
            oth >>= 1
        return point

class Encryptor():
    def __init__(self, curve, ln=256):
        self.G = Point(curve.G[0], curve.G[1], curve)
        self.ln = ln
        self.privk = 0
        
    def generate(self, rand_func=None):
        if rand_func is None:
            self.privk = int.from_bytes(os.urandom(self.ln//8), sys.byteorder)
        else:
            self.privk = rand_func(self.ln)
        
    def getPubK(self):
        assert self.privk, "private key is undefined, use \"generate\" to define it."
        return self.G * self.privk        
    
    def sign(self, message:bytes):
        message = int.from_bytes(sha256(message).digest(), sys.byteorder)
        r, s = 0, 0
        while not r or not s:
            k = ext_randint(1, self.G.curve.n)
            pnt = self.G*k
            r = pnt.x % self.G.curve.n
            s = ((message + r * self.privk) * mod_inverse(k, self.G.curve.n)) % self.G.curve.n
        return Point(r, s, self.G.curve)
    
    @staticmethod
    def verify(pubK:Point, message, signature:Point):
        message = int.from_bytes(sha256(message).digest(), sys.byteorder)
        G = Point(pubK.curve.G[0], pubK.curve.G[1], pubK.curve)
        r, s = signature.x, signature.y
        w = mod_inverse(s, pubK.curve.n)
        u1 = (message * w) % pubK.curve.n
        u2 = (r * w) % pubK.curve.n
        
        pnt = (G * u1) + (pubK * u2)
        if (r % pubK.curve.n) == (pnt.x % pubK.curve.n): return True
        else: return False
