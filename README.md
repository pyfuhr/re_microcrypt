# Cryptography for micropython
+ 🟩random for numbers >= 2*31
+ 🟩generator for primes number(using Pocklington primality test)
+ 🟩publik key encrypting data (RSA)
+ 🟩signing data (RSA, ECDSA)
+ 🟩xor data encrypting(base64)
+ 🟩recrypt certificate(RSAPrivK)
+ 🟨make recrypt certificate(RSAPubK)
+ 🟧Diffie–Hellman protocol
+ 🟧AES, DES, RC4
+ 🟧work with polynomials, finite field
+ 🟥Reed–Solomon error correction
+ 🟥BCH code

# RSA result*
| n-bits | avg time for one key gen | cycles |
| --- | --- | --- |
| 32 | 11.4 s | 10 |
| 64 | 12.2 s | 10 |
| 128 | 15.5 s | 10 |
| 256 | 45.6 s | 10 |

## Usage
<>

*tested at Raspberry Pi Pico Board RP2040 by WeAct Studio
