"""
Day 14 of Advent of Code: Extended Polymerization - by Thijs de Groot
"""
import sys

all_pairs = []
all_inserts = []

with open('input.txt', 'r', encoding='utf-8') as file:
    polymer = list(file.readline().strip())
    next(file)
    for index, line in enumerate(file):
        [pair, insert] = line.strip().split(' -> ')
        all_pairs.append(pair)
        all_inserts.append(insert)

for i in range(10):
    print(i)
    insert_list = []
    index_list = []
    for index, char in enumerate(polymer[:-1]):
        current_pair = ''.join([char, polymer[index + 1]])
        pair_index = all_pairs.index(current_pair)
        index_list.append(index)
        insert_list.append(all_inserts[pair_index])

    reversed_index_list = list(reversed(index_list))
    reversed_insert_list = list(reversed(insert_list))

    for j, insert_index in enumerate(reversed_index_list):
        polymer.insert(insert_index + 1, reversed_insert_list[j])

    # print(''.join(polymer))

print(len(polymer))
chars = set(polymer)
print(chars)

max_el = 0
min_el = sys.maxsize

for char in chars:
    current_count = polymer.count(char)
    print(f'cur: {current_count}, max: {max_el}, min: {min_el}')
    if current_count < min_el:
        min_el = current_count
    if current_count > max_el:
        max_el = current_count

print(f'answer 1: {max_el - min_el}')
