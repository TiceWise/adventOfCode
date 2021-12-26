"""
Day 25 of Advent of Code: Sea Cucumber - by Thijs de Groot
"""
import numpy as np

move_matrix = np.array([])

first_line = True

with open('input.txt', 'r', encoding='utf-8') as file:
    for line in file:
        cur_row = list(line.strip())
        if first_line:
            move_matrix = np.array(cur_row)
            first_line = False
        else:
            move_matrix = np.vstack([move_matrix, cur_row])

rows, cols = np.shape(move_matrix)
next_ver_move_matrix = move_matrix.copy()

moved = True
steps = 0
while moved:
    moved = False
    next_hor_move_matrix = next_ver_move_matrix.copy()
    for row in range(rows):
        for col in range(cols):
            next_col = 0 if col == cols - 1 else col + 1
            if next_ver_move_matrix[row, col] == '>' and next_ver_move_matrix[row, next_col] == '.':
                next_hor_move_matrix[row, col] = '.'
                next_hor_move_matrix[row, next_col] = '>'
                moved = True

    next_ver_move_matrix = next_hor_move_matrix.copy()
    for row in range(rows):
        for col in range(cols):
            next_row = 0 if row == rows - 1 else row + 1
            if next_hor_move_matrix[row, col] == 'v' and next_hor_move_matrix[next_row, col] == '.':
                next_ver_move_matrix[row, col] = '.'
                next_ver_move_matrix[next_row, col] = 'v'
                moved = True
    steps += 1

    # print(next_ver_move_matrix)
print(f'answer 1: {steps}')
