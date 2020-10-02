import sys


# Expresses number 1 as the difference between multiples
# of a and b using euclidean gcd
def gcd(a, b):
    if a == 0:
        return 0, 1
    else:
        y, x = gcd(b % a, a)
        return x - (b // a) * y, y


# Returns the modulo inverse of 2 numbers
# We don't check if the number are co-primes because the assignment implies
# that they already are.
def modulo_inverse(n, m):
    x, y = gcd(n, m)
    return x % m


# Encrypt a message using the super-increasing knapsack problem
def encrypt(key, data):
    for message in data:
        cipher = 0
        for i in range(len(message)):
            cipher += int(message[i]) * key[i]
        print(cipher)


# Returns a binary number based on the weights that fit into the knapsack
def solve_number(number, key):
    binary_form = ''
    # We go over the list of weights in reverse
    # and form the decrypted binary number
    for k in key:
        # If knapsack reached capacity, only pad with 0's
        if number <= 0:
            binary_form += '0'
            continue
        # If weight k doesn't fit into knapsack, pad with a 0
        if k > number:
            binary_form += '0'
            continue
        # Pad with 1 if the weight can be put into the knapsack
        binary_form += '1'
        # Update knapsack weight
        number -= k
    return binary_form


# Decrypts a message using the super-increasing knapsack problem
def decrypt(m, n, key, data):
    cipher = []
    # Multiply each cipher number with the modulo inverse of m
    for number in data:
        cipher.append((int(number[::-1], 2) * modulo_inverse(m, n)) % n)
    # Decode each cipher number
    for number in cipher:
        print(int(solve_number(number, key), 2))


# Reads input data and transforms it into binary.
def input_data():
    binary_data = []
    while True:
        line = sys.stdin.readline()
        if line:
            binary_data.append(format(int(line), '0b')[::-1])
        else:
            break
    return binary_data


# Read the desired process (i.e. either 'e' - encryption or 'd' - decryption)
process = input()

if process == 'e':
    # Read the public key
    public_key = [int(x) for x in input().split()]
    data = input_data()
    encrypt(public_key, data)
elif process == 'd':
    # Read m and n together with the super-increasing knapsack
    m, n = [int(x) for x in input().split()]
    super_knapsack = [int(x) for x in input().split()]
    data = input_data()
    decrypt(m, n, super_knapsack[::-1], data)
