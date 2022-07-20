from re_microcrypt.utils.num_sublib import gcd, modinv, generatePrime, ext_randint

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
    '''delete zeros'''
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
    
    def check(self, etext, data=None, hashfunc=None, hashedData=None):
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
        if not (hashedData is None):
            if self.encrypt(etext) == hashedData: return True
            else: return False
        raise ValueError('Not enought args: text + (data+hashfunc or hashedData)')

    def __str__(self):
        return str({'e': self.e, 'n': self.n})

class RSAPrivK:
    def __init__(self, d, n):
        self.d = d
        self.n = n

    def decrypt(self, etext):
        '''
        decrypt bytes with RSA algoritm
        decrypt(bytes) -> original bytes
        '''
        etext = int.from_bytes(etext, 'big')
        return del0(int.to_bytes(pow(etext, self.d, self.n), 1024, 'big'))
    
    def sign(self, data=None, hashfunc=None, hashedData=None):
        '''
        make a sign
        send it to the recipient to ensure the integrity and security of the message
        
        sign(bytes, hashfunc) -> signed message
            or
        sign(hashedData) -> signed message
        
        hashedData equals hashfunc(data)
        '''
        if not (data is None) and not (hashfunc is None):
            return self.decrypt(hashfunc(data))
        if not (hashedData is None):
            return self.decrypt(hashedData)
        raise ValueError('Not enought args: data+hashfunc or hashedData')

    def __str__(self):
        return str({'d': self.d, 'n': self.n})

    def write_priv_cert(self, name, ln=4096):
        '''
        create recrypt certificate
        write_priv_cert(file_name) -> file_name.cert in fs
        '''
        file = open(name + '.cert', 'wb')
        file.write(b'--------- ReCrypto Key ---------' + b'\n')
        file.write(str(ln).encode('ascii') + b'\n')
        file.write(b'Type: PrivK' + b'\n')
        
        data = to_b64(self.d.to_bytes(ln, 'big'))
        for chunk in range(len(data) // 32):
            file.write(data[chunk*32:(chunk+1)*32] + b'\n')
        if len(data) % 32 == 0:
            file.write(data[(chunk+1)*32:] + b'\n\n')
        else:
            file.write(b'\n')

        data = to_b64(self.n.to_bytes(ln, 'big'))
        for chunk in range(len(data) // 32):
            file.write(data[chunk*32:(chunk+1)*32] + b'\n')
        if len(data) % 32 == 0:
            file.write(data[(chunk+1)*32:] + b'\n')
                

        file.close()

    @staticmethod
    def read_priv_cert(name):
        '''
        create RSAPrivK object from recrypt certificate
        read_priv_cert(file_name) -> RSAPrivK
        '''
        file = open(name + '.cert', 'rb')
        data = file.read().split(b'\n')
        if data[0] == b'--------- ReCrypto Key ---------':
            ln = int(data[1].decode('ascii'))
            if data[2] == b'Type: PrivK':
                i = 3
                b64_d = b''
                while data[i] != b'':
                    b64_d += data[i]
                    i += 1
                i += 1
                b64_n = b''
                while data[i] != b'':
                    b64_n += data[i]
                    i += 1
        file.close()

        return RSAPrivK(int.from_bytes(from_b64(b64_d), 'big'),
            int.from_bytes(from_b64(b64_n), 'big'))
