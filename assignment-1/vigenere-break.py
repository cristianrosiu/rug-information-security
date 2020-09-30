import math
import sys
from collections import Counter


def input_number():
    while True:
        try:
            user_input = int(input())
        except ValueError:
            print("Not an integer")
            continue
        else:
            return user_input


def input_text():
    cipher = sys.stdin.read()
    return cipher


class VigenereBreaker:
    def __init__(self, cipher, lower, upper):
        self.cipher = (''.join(filter(str.isalpha, cipher))).lower()
        # Bounds of key length space
        self.lower = lower
        self.upper = upper
        # Vector that contains biggest SD (final result)
        self.maximum_vector = [(-sys.maxsize, [])]

    def shift(self, char):
        return chr((ord(char) - ord('a') - 4) % 26 + ord('a'))

    # Computes and returns standard deviation of a frequency vector
    def standard_deviation(self, vector):
        return math.sqrt((sum([x * x for x in vector]) / 26 - (sum(vector) / 26) ** 2))

    # Map each letter of the cipher to it's specific vector based on the assigned number
    # e.g. abcd cda -> 0123 401 -> [[a,d],[b,a],[c],[d],[c]] for bound = 5
    def map_cipher(self, bound):
        vectors = []
        for i in range(bound):
            sub_str = self.cipher[i::bound]
            vectors.append(dict(Counter(sub_str)))
        return vectors

    # Returns a vector which contains the most frequent letters found in each bin.
    def most_used_letters(self):
        return [max(vector, key=vector.get) for vector in self.maximum_vector[0][1]]

    # Prints results + key
    def break_cipher(self):
        for i in range(self.lower, self.upper + 1):
            stdev = 0
            # Computes list of vectors that are relate to each letter in the key
            vectors = self.map_cipher(i)

            # Compute sum of all vectors SD's
            for vector in vectors:
                stdev += self.standard_deviation(vector.values())

            # Keep track of maximum SD and the vectors associated with it
            if self.maximum_vector[0][0] < stdev:
                self.maximum_vector.pop()
                self.maximum_vector.append((stdev, vectors))

            # Print results
            stdev = "{:.2f}".format(stdev)
            print("The sum of", i, "std. devs:", stdev)

        key_letters = self.most_used_letters()
        # Decrypt key by shifting each letter from the top most used letters array by a specific distance. In this
        # case, because 'e' is considered most frequent letter in English alphabet, we shift by a distance of char - 'e'
        key = ""
        for letter in key_letters:
            key += self.shift(letter)

        print("")
        print("Key guess:")
        print(key)


if __name__ == '__main__':
    # Input bounds
    lower_bound = input_number()
    upper_bound = input_number()

    # Input text
    text = input_text()

    breaker = VigenereBreaker(text, lower_bound, upper_bound)
    breaker.break_cipher()