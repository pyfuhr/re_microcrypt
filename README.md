# RSA for micropython
## RSA on microcontroler
+ 🟩random for numbers >= 2*31
+ 🟩generator for primes number
+ 🟨encrypting text


+ ❗ Generator work slowly for 1024 bit keys

| n-bits | avg time for one key gen | cycles |
| --- | --- | --- |
| 256 | 45.6 s | 10 |

## Usage
```python
from re_microcrypt import RSA
a = RSA(256)
private = a.privk
public = a.pubk

enc_mes = public.encrypt(33)
private.decrypt(enc_mes) # return 33
```
