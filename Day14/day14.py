"""
Day 14 of Advent of Code: Extended Polymerization - by Thijs de Groot
"""

import sys

all_pair_counts = {}
all_pair_inserts = {}

# read input
with open('input.txt', 'r', encoding='utf-8') as file:
    polymer = list(file.readline().strip())
    next(file)
    for index, line in enumerate(file):
        [pair, insert] = line.strip().split(' -> ')
        all_pair_counts[pair] = 0
        all_pair_inserts[pair] = insert

# count starting pairs
for index, char in enumerate(polymer[:-1]):
    current_pair = ''.join([char, polymer[index + 1]])
    all_pair_counts[current_pair] += 1

# initialize all letters of the polymer
key_string = []
for keys in all_pair_counts:
    key_string.append(keys)
all_letters = set(list(''.join(key_string)))

# initialize letter counter dict
letter_count = {}
for letter in all_letters:
    letter_count[letter] = 0

cycles = 40  # 40 for part 2

for i in range(cycles):
    # Each pair results in two pairs, with the amount/count of the current pair
    # all changes happen simultaneously, so don't update the current, but update 'the new' counts
    new_all_pair_counts = all_pair_counts.copy()
    for current_pair_el in all_pair_counts.items():
        current_pair = current_pair_el[0]
        current_pair_count = current_pair_el[1]
        new_left_pair = ''.join([current_pair[0], all_pair_inserts[current_pair]])
        new_right_pair = ''.join([all_pair_inserts[current_pair], current_pair[1]])
        new_all_pair_counts[new_left_pair] += current_pair_count
        new_all_pair_counts[new_right_pair] += current_pair_count
        new_all_pair_counts[current_pair] -= current_pair_count

        all_pair_counts = new_all_pair_counts.copy()

# count letters: split all pairs into the corresponding letters and add them to the letter count
for current_pair_el in all_pair_counts.items():
    current_pair = current_pair_el[0]
    current_pair_count = current_pair_el[1]

    letter_count[current_pair[0]] += current_pair_count
    letter_count[current_pair[1]] += current_pair_count

# all letters are counted twice (left of one pair, right of another pair)...
# ...except the outer two letters, which are counted one less
letter_count[polymer[0]] += 1
letter_count[polymer[-1]] += 1

# half the letter count and track min and max:
max_el = 0
min_el = sys.maxsize

for letter in all_letters:
    current_count = letter_count[letter] // 2
    if current_count < min_el:
        min_el = current_count
    if current_count > max_el:
        max_el = current_count

print(f'answer: {max_el - min_el}')
