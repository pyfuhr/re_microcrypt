from binascii import a2b_base64 as from_b64
from binascii import b2a_base64 as to_b64
    
def xor_bytes(s, key, enc):
    r = b''
    sT = (s if enc else from_b64(s))
    ln = 0
    if len(sT) % len(key):
        sT += ext_randint(0, 2**(8*((len(key)-len(sT)%len(key))))-1).to_bytes(ln:=(len(key)-(len(sT)%len(key))), 'big')
    for i in range(len(sT)//len(key)):
        for j in range(len(key)):
            r += int.to_bytes(sT[i*len(key)+j]^key[j], 1, 'big')
    if ln:        
        r = r[:-ln]
    return to_b64(r) if enc else r
