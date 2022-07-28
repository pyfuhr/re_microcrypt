from re_microcrypt.utils.num_sublib import mod_inverse, generatePrime, ext_randint

class RSA():
    '''
    RSA class:
    generate rsa pub and priv keys
    
    RSA(ln=<length>) - create ln bits keys
    RSA(p=<p_>, q=<q_>) - create keys from generatrix p_ and q_
    
    return private(privk) and public keys(pubk)
    '''
    def __init__(self, **kwargs):
        ln = kwargs.get('ln')
        self.__p, self.__q = kwargs.get('p'), kwargs.get('q')
        if not ln is None:
            self.__p = generatePrime(ln)
            self.__q = generatePrime(ln)
            while self.__q == self.__p:
                self.__q = generatePrime(ln)
        self.n = self.__p*self.__q
        self.f = (self.__p-1)*(self.__q-1)
        self.e = 65537
        self.__d = mod_inverse(self.e, self.f)
        self.pubk = RSAPubK(self.e, self.n)
        self.privk = RSAPrivK(self.__d, self.n)

    def __repr__(self):
        print('Warning! it\'s your private key')
        return f'RSA(p={self.__p}, q={self.__q})'

    def __str__(self):
        return f'RSA object:{self.pubk}'

def del0(s:bytes):
    '''delete zeros from start bytes'''
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

    def encrypt(self, text:bytes):
        '''
        encrypt bytes with RSA algoritm
        encrypt(bytes) -> encrypted bytes
        '''
        text = int.from_bytes(text, 'big')
        return del0(int.to_bytes(pow(text, self.e, self.n), 1024, 'big'))
    
    def check(self, etext, data, hashfunc):
        '''
        compare sender and your sign
        
        check(recv_sign, data, hashfunc) -> boolean
            or
        check(recv_sign, hashedData) -> signed message
        
        hashedData equals hashfunc(data)
        '''
        if not (data is None) and not (hashfunc is None):
            if self.encrypt(etext) == hashfunc(data): return True
            else: return False
        
    def __str__(self):
        return str({'e': self.e, 'n': self.n})

    def __repr__(self):
        return f'RSAPubK({self.e}, {self.n})'

class RSAPrivK:
    def __init__(self, d, n):
        self.__d = d
        self.n = n

    def decrypt(self, etext):
        '''
        decrypt bytes with RSA algoritm
        decrypt(bytes) -> original bytes
        '''
        etext = int.from_bytes(etext, 'big')
        return del0(int.to_bytes(pow(etext, self.__d, self.n), 1024, 'big'))
    
    def sign(self, data=None, hashfunc=None):
        '''
        make a sign
        send it to the recipient to ensure the integrity and security of the message
        sign(bytes, hashfunc) -> signed message
        '''
        if not (data is None) and not (hashfunc is None):
            return self.decrypt(hashfunc(data))

    def __str__(self):
        return str('RSAPrivk str method called')

    def __repr__(self):
        print('Warning! it\'s your private key')
        return f'RSAPrivK({self.__d}, {self.n})'
    
print(RSA(ln=32))