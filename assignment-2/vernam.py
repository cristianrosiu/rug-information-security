import sys


def one_time_pad(plaintext, key):
    return bytes(a ^ b for a, b in zip(plaintext, key))


key, text = sys.stdin.buffer.read().split(b"\xff", 1)
sys.stdout.buffer.write(one_time_pad(text, key))