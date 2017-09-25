import os
from Algorithms import Alg

BYTES = 4


class RSA:
    def __init__(self, p=0, q=0):
        self.p = p
        self.q = q
        self.n = 0
        self.e = 0
        self.d = 0
        if not p * q:
            self.genkeys()
        self.initialize()

    def genkeys(self):
        self.p = int.from_bytes(os.urandom(BYTES), byteorder='big', signed=False)
        while not Alg.is_prime(self.p):
            self.p -= 1
        self.q = int.from_bytes(os.urandom(BYTES), byteorder='big', signed=False)
        while not Alg.is_prime(self.q):
            self.q -= 1

    def initialize(self, e=0):
        self.n = self.p * self.q
        if e == 0:
            for i in range(2, self.phi_n):
                try:
                    self.d = Alg.mul_inverse(i, self.phi_n)
                    while self.d < 0:
                        self.d += self.phi_n
                    self.e = i
                    break
                except ValueError:
                    pass
        else:
            self.e = e
            self.d = Alg.mul_inverse(e, self.phi_n)
            while self.d < 0:
                self.d += self.phi_n

    @property
    def pub_key(self):
        return self.e, self.n

    def encrypt(self, msg):
        return Alg.mod_pow(msg, self.e, self.n)

    def decrypt(self, msg):
        return Alg.mod_pow(msg, self.d, self.n)

    def check(self, msg=111):
        enc = self.encrypt(msg)
        dec = self.decrypt(enc)
        return msg == dec

    @property
    def phi_n(self):
        return (self.p - 1) * (self.q - 1)

    @classmethod
    def break_RSA(cls, e, n):
        d = Alg.pollard_factorize(n)
        if d == 0:
            raise ValueError('n is prime')
        if n % d != 0:
            raise ValueError(' n%d != 0')

        rsa = RSA(d, n // d)
        rsa.initialize(e)
        if not rsa.check():
            raise ValueError('RSA inconsistent')
        return rsa


e, n = 937513, 638471
msg = 12345
rsa = RSA.break_RSA(e, n)

enc = rsa.encrypt(msg)
dec = rsa.decrypt(enc)

print(dec == msg)
