# RSA for micropython
## RSA on microcontroler
+ 🟩random for numbers >= 2*31
+ 🟩generator for primes number
+ 🟩encrypting bytes

| n-bits | avg time for one key gen | cycles |
| --- | --- | --- |
| 32 | 11.4 s | 10 |
| 64 | 12.2 s | 10 |
| 128 | 15.5 s | 10 |
| 256 | 45.6 s | 10 |

## Usage
```python
from re_microcrypt import RSA, RSAPubK
from hashlib import sha256
rsa = RSA(ln=128)
encdata = a.pubk.encrypt(b'hi')
print(a.privk.decrypt(o))
>>> b'hi'
signed_data = a.privk.sign(hashedData=sha256(b'mumei').digest())
print(a.pubk.check(signed_data, hashedData=sha256(b'mumei').digest()))
>>> True
```
