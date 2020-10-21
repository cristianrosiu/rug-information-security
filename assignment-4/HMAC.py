import sys
from tiger_hash import Tiger


# Function to xor each bit in byte1 with each bit in byte2
def xor_bytes(byte1, byte2):
    return bytes(a ^ b for a, b in zip(byte1, byte2))


def pad(text):
    # Number of zeros to pad
    while len(text) % 64 != 0:
        text = b'\x00' + text

    return text


if __name__ == "__main__":
    # key, message = sys.stdin.buffer.read().split(b"\xff", 1)
    tiger = Tiger()

    key = pad(b"testkey")
    message = b"simplemessage"

    ipad = b"\x36"
    opad = b"\x5c"

    h2 = tiger.hash(xor_bytes(key, ipad)+message)
    h1 = xor_bytes(key, opad) + h2
    print(h1)

    f = open("0.out", 'rb')
    stra = b''
    byte = f.read(1)
    while byte:
        stra += byte
        byte = f.read(1)

    print(stra)

