from Algorithms import Alg
from RSA import RSA

# Question 1
n1 = 1013
print('Question 1: ', Alg.is_prime_idiot(n1))
print()

# Question 2
print('Question 2: ', Alg.is_prime(n1))
print()

# Question 3

# Question 4
a = Alg.euclidean(499017086208, 676126714752)['gcd']  # Output: 93312
b = Alg.euclidean(5988737349, 578354589)['gcd']  # Output: 9

print('Question 4: ')
print('a = ', a)
print('b = ', b)
print()

# Question 5
x = Alg.mul_inverse(342952340, 4230493243) # Output: 583739113
print('Question 5: ')
print('x = ', x)
print()

#Question 6
e, n = 937513, 638471
msg = 12345
rsa = RSA.break_RSA(e, n)

enc = rsa.encrypt(msg)
dec = rsa.decrypt(enc)

print('Question 6')
print('Initial Message: ', msg)
print('Encrypted: ', enc)
print('Decrypted: ', dec)
print('Correct ? ' ,dec == msg)
