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


def standard_deviation(vector):
    return math.sqrt(sum(map(lambda x: x * x, vector)) / 26 - (sum(vector) / 26) ** 2)


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


def map_text_to_k(text, bound):
    mapping = []
    k = 0
    for i in range(len(text)):
        if k == bound:
            k = 0
        if text[i].isalpha():
            mapping.append((k, text[i]))
            k = k + 1
        else:
            mapping.append((-1, '/'))

    return mapping


lower_bound = input_number()
upper_bound = input_number()

text = input_text()
results = [(-sys.maxsize, [])]
for i in range(lower_bound, upper_bound + 1):
    sd = 0
    text_map = map_text_to_k(text, i)
    vectors = [[tup[1] for tup in text_map if tup[0] == j] for j in range(i)]

    for vector in vectors:
        sd += statistics.stdev([vector.count(letter) for letter in vector])
    if results[0][0] < sd:
        results.pop()
        results.append((sd, vectors))
    print("The sum of", i, "std. devs:", sd)

most_used_letters = [collections.Counter(vector).most_common(1)[0][0] for vector in results[0][1]]
print(most_used_letters)
result = [chr(((ord('a') + (ord(letter) - ord('e'))) - ord('a')) % 26 + ord('a')) for letter in most_used_letters]
print(str(result))
