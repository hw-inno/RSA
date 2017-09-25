import math

class Alg:
    @classmethod
    def is_prime(cls, num):
        if num == 2:
            return True

        if num % 2 == 0:
            return False

        for i in range(3, math.ceil(math.sqrt(num)), 2):
            if num % i == 0:
                return False

        return True

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
    def pollard_factorize(cls, n):
        def g(x):
            return (x*x+1)%n
        x = 2
        y = 2
        d = 1
        while d==1:
            x = g(x)
            y = g(g(y))
            d = Alg.euclidean(abs(x - y), n)['gcd']
        if d == n:
            return 0
        return d

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