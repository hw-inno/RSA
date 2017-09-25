import os
import sympy

BYTES = 4

class RSA:
    def __init__(self, p = 0, q = 0):
        self.p = p
        self.q = q
        self.n = 0
        self.e = 0
        self.d = 0
        if not p*q:
            self.genkeys()
        self.initialize()
        
    def genkeys(self):
        self.p = int.from_bytes(os.urandom(BYTES), byteorder='big', signed=False)
        while not sympy.isprime(self.p):
            self.p -= 1
        self.q = int.from_bytes(os.urandom(BYTES), byteorder='big', signed=False)
        while not sympy.isprime(self.q):
            self.q -= 1

    def initialize(self, e = 0):
        self.n = self.p*self.q
        if e==0:
            for i in range(2, self.phi_n):
                try:
                    self.d = RSA.mul_inverse(i, self.phi_n)
                    while self.d<0:
                        self.d += self.phi_n
                    self.e = i
                    break
                except ValueError:
                    pass
        else:
            self.e = e
            self.d = RSA.mul_inverse(e, self.phi_n)
            while self.d<0:
                self.d += self.phi_n

    @property
    def pub_key(self):
        return self.e, self.n

    def encrypt(self, msg):
        return RSA.mod_pow(msg, self.e, self.n)

    def decrypt(self, msg):
        return RSA.mod_pow(msg, self.d, self.n)

    def check(self, msg=111):
        enc = self.encrypt(msg)
        dec = self.decrypt(enc)
        return msg == dec

    @property
    def phi_n(self):
        return (self.p-1)*(self.q-1)

    @classmethod
    def mod_pow(cls, base, power, MOD):
        result = 1
        while power > 0:
            # If power is odd
            if power % 2 == 1:
                result = (result * base) % MOD
            # Divide the power by 2
            power = power // 2
            # Multiply base to itself
            base = (base * base) % MOD
        return result

    @classmethod
    def euclidean(cls, a, b):
        s = 0
        old_s = 1
        t = 1  
        old_t = 0
        r = b   
        old_r = a

        while r != 0:
            quotient = old_r // r
            old_r, r = (r, old_r - quotient * r)
            old_s, s = (s, old_s - quotient * s)
            old_t, t = (t, old_t - quotient * t)

        return {'bezout': [old_s, old_t], 'gcd': old_r, 'quotients': [t, s]}
        
    @classmethod
    def mul_inverse(cls, a, n):
        euc = cls.euclidean(a, n)
        if euc['gcd'] != 1:
            raise ValueError('gcd != 1')
        return euc['bezout'][0]

    @classmethod
    def break_RSA(cls, e, n):
        d = RSA.pollard_factorize(n)
        if d==0:
            raise ValueError('n is prime')
        if n%d != 0:
            raise ValueError(' n%d != 0')

        rsa = RSA(d, n//d)
        rsa.initialize(e)
        if not rsa.check():
            raise ValueError('RSA inconsistent')
        return rsa 

    @classmethod
    def pollard_factorize(cls, n):
        def g(x):
            return (x*x+1)%n
        x = 2
        y = 2
        d = 1
        while d==1:
            x = g(x)
            y = g(g(y))
            d = RSA.euclidean(abs(x-y), n)['gcd']
        if d == n:
            return 0
        return d

e, n = 937513,	638471
msg = 12345
rsa = RSA.break_RSA(e, n)

enc = rsa.encrypt(msg)
dec = rsa.decrypt(enc)

print(dec == msg)


