from num_sublib import gcd, modinv, generatePrime

class RSA():
    def __init__(self, len):
        self.p = generatePrime(len)
        self.q = generatePrime(len)
        while self.q == self.p:
            self.q =generatePrime(len)
        self.n = self.p*self.q
        self.f = (self.p-1)*(self.q-1)
        self.e = 65537
        self.d = modinv(self.e, self.f)
        self.pubk = PubK(self.e, self.n)
        self.privk = PrivK(self.d, self.n)


class PubK():
    def __init__(self, e, n):
        self.e = e
        self.n = n
    def encrypt(self, text):
        return pow(text, self.e, self.n)

class PrivK():
    def __init__(self, d, n):
        self.d = d
        self.n = n
    def decrypt(self, etext):
        return pow(etext, self.d, self.n)
