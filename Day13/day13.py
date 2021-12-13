"""
Day 13 of Advent of Code: Transparent Origami - by Thijs de Groot
"""

import numpy as np
import matplotlib.pyplot as plt

all_x = []
all_y = []

all_fold_axis = []
all_xy_fold_axis = []


def plot_paper(bool_paper_to_plot):
    """
    Creates a heatmap plot of input boolean numpy array
    :param bool_paper_to_plot:
    :return:
    """
    paper = np.zeros_like(bool_paper_to_plot).astype(int)
    paper[bool_paper_to_plot] = 100
    paper[np.invert(bool_paper_to_plot)] = 0
    plt.imshow(paper, cmap='hot')
    plt.show()


with open('input.txt', 'r', encoding='utf-8') as file:
    for line in file:
        if line[0:4] == "fold":
            [xy_axis_string, axis_string] = line.strip().split('=')
            all_fold_axis.append(int(axis_string))
            all_xy_fold_axis.append(xy_axis_string[-1])
        elif line != '\n':
            [x, y] = line.strip().split(',')
            all_x.append(int(x))
            all_y.append(int(y))

# X are columns, Y are rows
bool_paper = np.zeros([max(all_y) + 1, max(all_x) + 1]).astype(bool)

# set the dots
for index, x in enumerate(all_x):
    bool_paper[all_y[index], x] = True

# fold
for index, fold_axis in enumerate(all_fold_axis):
    if all_xy_fold_axis[index] == 'y':
        top_half = bool_paper[:fold_axis, :]
        bottom_half = bool_paper[fold_axis + 1:, :]

        top_half_shape = np.shape(top_half)
        bottom_half_shape = np.shape(bottom_half)
        if top_half_shape[0] > bottom_half_shape[0]:
            bottom_half = np.vstack([bottom_half, np.zeros_like(bottom_half[1, :])])

        bool_paper = top_half + np.flipud(bottom_half)
    if all_xy_fold_axis[index] == 'x':
        left_half = bool_paper[:, :fold_axis]
        right_half = bool_paper[:, fold_axis + 1:]
        bool_paper = left_half + np.fliplr(right_half)

    if index == 0:
        print(f'answer 1: {np.sum(bool_paper)}')

plot_paper(bool_paper)
