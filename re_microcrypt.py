from num_sublib import gcd, modinv, generatePrime

class RSA():
    def __init__(self, **kwargs):
        ln = kwargs.get('ln')
        self.p, self.q = kwargs.get('p'), kwargs.get('q')
        if not ln is None:
            self.p = generatePrime(ln)
            self.q = generatePrime(ln)
            while self.q == self.p:
                self.q = generatePrime(ln)
        self.n = self.p*self.q
        self.f = (self.p-1)*(self.q-1)
        self.e = 65537
        self.d = modinv(self.e, self.f)
        self.pubk = RSAPubK(self.e, self.n)
        self.privk = RSAPrivK(self.d, self.n)

def del0(s):
    k = 0
    for i in range(len(s)):
        if s[i] == 0:
            k += 1
        else:
            break
    return s[k:]

class RSAPubK:
    def __init__(self, e, n):
        self.e = e
        self.n = n

    def encrypt(self, text):
        text = int.from_bytes(text, 'big')
        return del0(int.to_bytes(pow(text, self.e, self.n), 1024, 'big'))
    
    def check(self, text, data=None, hashfunc=None, hashedData=None):
        if not (data is None) and not (hashfunc is None):
            if self.encrypt(text) == hashfunc(data): return True
            else: return False
        if not (hashedData is None):
            if self.encrypt(text) == hashedData: return True
            else: return False
        raise ValueError('Not enought args: text + (data+hashfunc or hashedData)')

    def __str__(self):
        return str({'e': self.e, 'n': self.n})


class RSAPrivK:
    def __init__(self, d, n):
        self.d = d
        self.n = n

    def decrypt(self, etext):
        etext = int.from_bytes(etext, 'big')
        return del0(int.to_bytes(pow(etext, self.d, self.n), 1024, 'big'))
    
    def sign(self, data=None, hashfunc=None, hashedData=None):
        if not (data is None) and not (hashfunc is None):
            return self.decrypt(hashfunc(data))
        if not (hashedData is None):
            return self.decrypt(hashedData)
        raise ValueError('Not enought args: data+hashfunc or hashedData')

    def __str__(self):
        return str({'d': self.d, 'n': self.n})

