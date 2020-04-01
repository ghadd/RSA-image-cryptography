from PIL import Image
import numpy as np
import io

initial_image_path = '/home/ghadd/Downloads/pic.jpg'
cipher_path = '/home/ghadd/Downloads/pic_cipher.txt'
deciphered_image_path = '/home/ghadd/Downloads/pic_decipher.jpg'

def gcd(a, b):
	if b == 0:
		return a
	else:
		return gcd(b, a%b)

def is_prime(a):
	if a > 1:
		if a == 2:
			return True
		else:
			for i in range(2, int(a**0.5) + 1):
				if a % i == 0:
					return False
		return True
	return False

def mod_exp(m, e, n):
	if e == 0:
		return 1
	elif e % 2 == 0:
		return (mod_exp(m, e / 2, n))**2 % n
	else:
		return ((m % n) * mod_exp(m, e - 1, n)) % n

def get_bytes(filename):
	with open(filename, 'rb') as file:
		return bytearray(file.read())

def write_file(filename, data):
	with open(filename, 'w') as file:
		for peace in data:
			file.write(f'{peace}-')

def read_file(filename):
	with open(filename, 'r') as file:
		return [int(i) for i in file.read().split('-')[:-1]]


data = get_bytes(initial_image_path)

print("Here are some primes")
print(list(filter(is_prime, range(500, 1000))))

p = int(input("Prime 1: "))
q = int(input("Prime 2: "))

assert is_prime(p) and is_prime(q)

n = p * q
t = (p - 1) * (q - 1)

e = d = 1

for i in range(2, t):
	if gcd(i, t) == 1:
		e = i
		break

for i in range(1, 10):
	x = 1 + i * t
	if x % e == 0:
		d = x / e
		break

public_key = [e, n]
private_key = [d, n]

cipher = []
for m in data:
	cipher.append(mod_exp(m, public_key[0], public_key[1]))

print("Encryption done")
write_file(cipher_path, cipher)
print("Cipher file saved")

# ---------------------------------------------------------------------------

decipher = []
read_cipher = read_file(cipher_path)
for m in read_cipher:
	decipher.append(mod_exp(m, private_key[0], private_key[1]))

decipher = bytearray(decipher)
print("Decrytpion done")

assert data == decipher, "Decrytpion error. This may happen when you use a wrong private key or excryption was done with small primes"

img = Image.open(io.BytesIO(bytearray(decipher)))
img.save(deciphered_image_path)

print("Decrytpted image saved")