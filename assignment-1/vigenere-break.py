import math
import statistics
import sys
import collections


def input_number():
    while True:
        try:
            user_input = int(input())
        except ValueError:
            print("Not an integer")
            continue
        else:
            return user_input


def sqr(x):
    return x * x


def standard_deviation(vector):
    return math.sqrt((sum([x * x for x in vector]) / 26 - sqr(sum(vector) / 26)))


def input_text():
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    result = '\n'.join(lines)

    return result


# Map each letter of a text to numbers (e.g. "This is a sentence" -> 1234 51 2 345123451 , bound = 5)
def map_text_to_k(text, bound):
    mapping = []
    k = 0
    for i in range(len(text)):
        # If k reached bound, reset k to start again
        if k == bound:
            k = 0

        # If character is a letter just add tuple (number, character) to result
        mapping.append((k, text[i]))
        k = k + 1

    return mapping


# Shifts a character based on letter frequency
def shift(char):
    # See how much the encrypted letter was shifted by.
    shift_value = ord(char) - ord('e')
    if char.isupper():
        shift_value = ord(char) - ord('E')
        return chr(shift_value % 26 + ord('A'))
    return chr(shift_value % 26 + ord('a'))


# Input bounds
lower_bound = input_number()
upper_bound = input_number()

# Input text
text = input_text()
text = ''.join(filter(str.isalpha, text))

results = [(-sys.maxsize, [])]  # Used to get the vectors array with biggest Standard Deviation
for i in range(lower_bound, upper_bound + 1):
    sd = 0
    text_map = map_text_to_k(text, i)

    # Compute the list of vectors
    vectors = [[tup[1] for tup in text_map if tup[0] == j] for j in range(i)]
    for vector in vectors:
        frequency_vector = [vector.count(letter) for letter in set(vector)]
        sd += standard_deviation(frequency_vector)
    if results[0][0] < sd:
        results.pop()
        results.append((sd, vectors))
    sd = "{:.2f}".format(sd)
    print("The sum of", i, "std. devs:", sd)

most_used_letters = [collections.Counter(vector).most_common(1)[0][0] for vector in results[0][1]]

result = [shift(letter) for letter in most_used_letters]
print(text)
print(results)
print(most_used_letters)
print()
print("Key guess:")
for char in result:
    print(char, end='')
print()
