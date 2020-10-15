from sys import stdin, stdout


# Function to xor each bit in byte1 with each bit in byte2
def xor_bytes(byte1, byte2):
    return bytes(a ^ b for a, b in zip(byte1, byte2))


# Apply feistel algorithm in a recursive manner
def feistel(lhs, rhs, key_blocks, i):
    if i < len(key_blocks):
        key = key_blocks[i] + key_blocks[i]
        lhs, rhs = rhs, xor_bytes(lhs, key)
        return feistel(lhs, rhs, key_blocks, i + 1)
    return lhs + rhs


if __name__ == '__main__':
    process, key, text = stdin.buffer.read().split(b"\xff", 2)
    # Split the raw text in chunks of 8
    text_blocks = [text[i:i + 8] for i in range(0, len(text), 8)]
    # Split the raw key in chunks of 4
    key_blocks = [key[i:i + 4] for i in range(0, len(key), 4)]

    result = b""
    for block in text_blocks:
        # Divide the 8 bytes block into left side and right side
        lhs, rhs = block[0:4], block[4:8]
        # Append to the final result, the outcome of feistel rounds
        result += feistel(lhs, rhs, key_blocks, 0)
    stdout.buffer.write(result)
