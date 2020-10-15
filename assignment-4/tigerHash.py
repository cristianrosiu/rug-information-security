import sys
from sboxes import t1, t2, t3, t4

def inner_round(block, a, b, c, m):
    mask = 0xFFFFFFFFFFFFFFFF
    c = c ^ block
    c = c & mask

    c_array = c.to_bytes(8, 'little')
    a -= t1[c_array[0]] ^ t2[c_array[2]] ^ t3[c_array[4]] ^ t4[c_array[6]]
    b += t4[c_array[1]] ^ t3[c_array[3]] ^ t2[c_array[5]] ^ t1[c_array[7]]
    b = b * m

    a = a & mask
    b = b & mask
    c = c & mask

    return a, b, c


def outer_round(blocks, a, b, c, m, i=0):
    if i >= 8:
        return a, b, c
    if i == 0 or i == 3 or i == 6:
        a, b, c = inner_round(blocks[i], a, b, c, m)
        return outer_round(blocks, b, c, a, m, i + 1)
    if i == 1 or i == 4:
        b, c, a = inner_round(blocks[i], a, b, c, m)
        return outer_round(blocks, c, a, b, m, i + 1)
    if i == 2 or i == 5:
        c, a, b = inner_round(blocks[i], a, b, c, m)
        return outer_round(blocks, a, b, c, m, i + 1)
    if i == 7:
        b, c, a = inner_round(blocks[i], a, b, c, m)
        return outer_round(blocks, a, b, c, m, i + 1)


def key_schedule(w):
    mask = 0xFFFFFFFFFFFFFFFF
    w[0] = (w[0] - (w[7] ^ 0xA5A5A5A5A5A5A5A5) & mask) & mask
    w[1] = w[1] ^ w[0]
    w[2] = (w[2] + w[1]) & mask
    w[3] = (w[3] - (w[2] ^ (~w[1] & mask) << 19) & mask) & mask
    w[4] = w[4] ^ w[3]
    w[5] = (w[5] + w[4]) & mask
    w[6] = (w[6] - (w[5] ^ (~w[4] & mask) >> 23) & mask) & mask
    w[7] = w[7] ^ w[6]
    w[0] = (w[0] + w[7]) & mask
    w[1] = (w[1] - (w[0] ^ (~w[7] & mask) << 19) & mask) & mask
    w[2] = w[2] ^ w[1]
    w[3] = (w[3] + w[2]) & mask
    w[4] = (w[4] - (w[3] ^ (~w[2] & mask) >> 23) & mask) & mask
    w[5] = w[5] ^ w[4]
    w[6] = (w[6] + w[5]) & mask
    w[7] = (w[7] - (w[6] ^ 0x0123456789ABCDEF) & mask) & mask


def split_text(text):
    return [text[i:i + 64] for i in range(0, len(text), 64)]


def pad(text):
    text_length = len(text)
    original_length = len(text)

    # Pad with 0x01
    text += b'\x01'
    text_length += 1

    # Number of zeros to pad
    zero_count = 0
    if text_length % 64 <= 56:
        zero_count = abs(text_length % 64 - 56)
    else:
        while text_length % 64 != 56:
            zero_count += 1
            text_length += 1

    # Pad with zeros
    for i in range(zero_count):
        text += b'\x00'
        text_length += 1

    weird_bit = (original_length * 8).to_bytes(8, 'little')

    text += weird_bit
    return text


def hash(text):
    a = 0x0123456789ABCDEF
    b = 0xFEDCBA9876543210
    c = 0xF096A5B4C3B2E187
    mask = 0xFFFFFFFFFFFFFFFF

    a_original = a
    b_original = b
    c_original = c

    blocks = split_text(pad(text))
    for block in blocks:
        split = [block[i:i + 8] for i in range(0, len(block), 8)]
        w = [int.from_bytes(b, byteorder='little') for b in split]
        a, b, c = outer_round(w, a, b, c, 5)
        key_schedule(w)
        c, a, b = outer_round(w, c, a, b, 7)
        key_schedule(w)
        b, c, a = outer_round(w, b, c, a, 9)

    return a ^ a_original, (b - b_original) & mask, (c + c_original) & mask


if __name__ == '__main__':
    text = sys.stdin.buffer.read()

    a, b, c = hash(text)
    sys.stdout.buffer.write(a.to_bytes(8, 'little') + b.to_bytes(8, 'little') + c.to_bytes(8, 'little'))
