import numpy as np


def add_to_basin(row, col):
    if height_map_with_outline[row, col] >= 9:
        return 0
    else:
        height_map_with_outline[row, col] = 11  # make sure we don't come here again
        return 1 + add_to_basin(row - 1, col) + add_to_basin(row + 1, col) + add_to_basin(row, col - 1) + add_to_basin(
            row, col + 1)


array = []

with open('input.txt') as file:
    for line in file:
        array.append(list(line.strip()))
height_map = np.array(array).astype(int)

number_of_rows, number_of_cols = np.shape(height_map)

height_map_with_outline = np.ones([number_of_rows + 2, number_of_cols + 2]).astype(int) * 10
height_map_with_outline[1:-1, 1:-1] = height_map

sum_of_low_points = 0
basin_sizes = np.array([])

for row in range(1, number_of_rows + 1):
    for col in range(1, number_of_cols + 1):
        current = height_map_with_outline[row, col]
        up = height_map_with_outline[row - 1, col]
        down = height_map_with_outline[row + 1, col]
        left = height_map_with_outline[row, col - 1]
        right = height_map_with_outline[row, col + 1]
        if current < up and current < down and current < left and current < right:
            sum_of_low_points += current + 1
            basin_sizes = np.append(basin_sizes, add_to_basin(row, col)).astype(int)

sorted_basin_sizes = -np.sort(-basin_sizes)
print(f'answer 1: {sum_of_low_points}')
print(f'answer 2: {sorted_basin_sizes[0] * sorted_basin_sizes[1] * sorted_basin_sizes[2]}')
