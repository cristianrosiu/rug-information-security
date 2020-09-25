# Problem number 5 practical 1
import sys
import math as m
import numpy as np
from collections import Counter


# Class that when given the key size implements functions to calculate vector frequencies and std
class KeySize:
    def __init__(self, length):
        self.size = length
        self.vectors = []
        self.std = 0

    # Calculate the different vector frequencies
    def calculate_vector_frequencies(self, text):
        for i in range(self.size):
            string = text[i::self.size]
            print(string)
            # Ana are mere
            frequency = dict(Counter(string))
            self.vectors.append((string, frequency))


    # Calculate the sum of the std of all the vectors of the given key
    def calculate_std(self):
        for i in range(self.size):
            values = np.array(list(self.vectors[i][1].values()))
            std = m.sqrt((np.sum(values * values) / 26) - ((np.sum(values) / 26) * (np.sum(values) / 26)))
            self.std += std
        return self.std


# Scan the input numbers and text, also remove all the special characters and numbers
def scan_input():
    lower = int(sys.stdin.readline().strip())
    upper = int(sys.stdin.readline().strip())
    cipher = sys.stdin.read()
    final = ""
    for ch in cipher:
        if ch.isalnum() and not ch.isdigit():
            final += ch
    return lower, upper, final.lower()


# Function that iterates over all the different key sizes and finds the best one
def get_best_key_size(lower, upper, cipher):
    keys_std = []
    for i in range(lower, upper + 1):
        key = KeySize(i)
        key.calculate_vector_frequencies(cipher)
        print(key.vectors)
        std = key.calculate_std()
        keys_std.append((i, std))
    return max(keys_std, key=lambda item: item[1]), keys_std


# Given the best key size find the keyword used to generate cipertext
def best_key(key_size, cipher):
    key = KeySize(key_size)
    key.calculate_vector_frequencies(cipher)
    final = ""
    for i in range(key_size):
        vector_frequency = key.vectors[i][1]
        letter = best_letter(vector_frequency)
        final += letter
    return final


# Get the best letter for the vector based on the frequency of the letters
def best_letter(frequency):
    most_frequent_letter = max(frequency, key=frequency.get)
    ascii_of_letter = ord(most_frequent_letter) - ord('e') + 97
    if ascii_of_letter < 97:
        ascii_of_letter += 26
    return chr(ascii_of_letter)


# Print answer in the correct format
def print_answer(list, keyword):
    for e in list:
        std = "{:.2f}".format(e[1])
        print("The sum of " + str(e[0]) + " std. devs: " + std)
    print("")
    print("Key guess:")
    print(keyword)


if __name__ == '__main__':
    lower, upper, cipher = scan_input()
    best, all_keys_list = get_best_key_size(lower, upper, cipher)
    keyword = best_key(best[0], cipher)
    print_answer(all_keys_list, keyword)