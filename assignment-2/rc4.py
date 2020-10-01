import sys


def key_scheduling(key):
    s = list(range(256))

    j = 0
    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) % 256
        s[i], s[j] = s[j], s[i]
    return s


def pseudo_random_generation(s):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + s[i]) % 256

        s[i], s[j] = s[j], s[i]
        k = s[(s[i] + s[j]) % 256]
        yield k


def RC4(key):
    return pseudo_random_generation(key_scheduling(key))


def to_bytes(number):
    binary_form = []
    while number > 1:
        binary_form.append(number % 2)
        number = number // 2
    return binary_form[::-1]


data_file = open("0.out", "rb")

text = data_file.readline().split(b"\xff", 1)


for byte in text[0]:
    print(byte, end=' ')
print('\n')

# key, text = sys.stdin.buffer.readline().split(b"\xff", 1)
data_file = open("0.in", "rb")
key, text = data_file.readline().split(b"\xff", 1)
key = [i for i in key]
key_stream = RC4(key)


for i in text:
    print(bytearray(str(i ^ next(key_stream)),'utf-8'))

