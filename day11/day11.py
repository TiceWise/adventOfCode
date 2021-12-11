"""
Day 11 of advent of code: Dumbo Octopus - by Thijs de Groot
"""

import numpy as np

array = []

with open('input.txt', 'r', encoding='utf-8') as file:
    for line in file:
        array.append(list(line.strip()))
energy_map = np.array(array).astype(int)

number_of_rows, number_of_cols = np.shape(energy_map)

energy_map_with_outline = np.ones([number_of_rows + 2, number_of_cols + 2]).astype(int) * 10
energy_map_with_outline[1:-1, 1:-1] = energy_map

STEPS = 500
FLASHES = 0
for n in range(STEPS):
    energy_map_with_outline[1:-1, 1:-1] += 1

    flashed_map = np.zeros_like(energy_map_with_outline)
    while True:
        flash_rows, flash_cols = np.where(energy_map_with_outline > 9)
        previous_number_of_flashes = np.sum(flashed_map)
        for index, row in enumerate(flash_rows):
            col = flash_cols[index]
            if 0 < row <= number_of_rows and 0 < col <= number_of_cols and flashed_map[row, col] == 0:
                energy_map_with_outline[row - 1:row + 2, col - 1:col + 2] += 1
                flashed_map[row, col] = 1
        if np.sum(flashed_map) == previous_number_of_flashes:
            break

    FLASHES += np.sum(flashed_map)
    energy_map_with_outline[np.where(energy_map_with_outline > 9)] = 0  # also include outline to keep that a bit clean

    if n == 100:
        print(f'answer 1: {FLASHES}')
    if np.sum(energy_map_with_outline[1:-1, 1:-1]) == 0:
        print(f'answer 2: {n + 1}')
        break
