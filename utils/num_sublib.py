import random
import time


def extgcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extgcd(b % a, a)
        return (g, x - (b // a) * y, y)


def mod_inverse(a, n):
    while a < 0:
        a += n
    old_r, r = n, a
    old_t, t = 0, 1
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_t, t = t, old_t - quotient * t
    if old_r > 1:
        raise Exception('no mod inv')
    if old_t < 0:
        old_t += n
    return old_t


def ext_randint(a, b, step=8):
    r, q = 0, []
    c = b - a
    flag = 0
    d = 0
    for i in range(1024):
        if c // (2**(step*i)) == 0:
            d = i-1
            break
    
    if d == 0:
        return random.randint(a, b)
    else:
        for i in range(d+1):
            q.append((c >> (d-i)*step)%2**step)

        for i in range(d+1):
            if flag == i:
                tmp = random.randint(0, q[i])
                r += (tmp * 2**(step*(d-i)))
                if tmp == q[i]:
                    flag += 1
            else:
                tmp = random.randint(0, 2**step-1)
                r += tmp * 2**(step*(d-i))
    if r+a>b: raise Exception('Err: rand')
    return r+a


def gcd(a, b):
    while b:
        a, b = b, a%b
    return a


def getPrimesToN(n:int) -> list:
    res = [2, 3]
    for i in range(4, n):
        flag = True
        for j in res:
            if i % j == 0:
                flag = False
                break

        if flag: res.append(i)
    return res


def div_to_anyList(n:int, l:list):
    flag = False
    for i in l:
        if n % i == 0:
            flag = True
            break
    return flag


def generatePrime(n: int, primes=None, s=None):
    limit = 2**n
    if primes is None: primes= getPrimesToN(1000)
    if s is None: s= primes[-1]
    while s < limit:
        low, high = (s+1) >> 1, (s << 1)+1
        while True:
            r = ext_randint(low, high) << 1
            n = s * r + 1
            #if div_to_anyList(n, primes): continue
            while True:
                a = ext_randint(2, n-1)
                if pow(a, n-1, n) != 1: break # тест простоты Ферма
                d = gcd((pow(a, r, n)-1) % n, n) # критерий Поклингтона
                if d != n:
                    if d == 1: s = n
                    break
            if s == n: break
    return s


millis = int(round(time.time()))
random.seed(millis)
