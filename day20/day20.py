"""
Day 20 of Advent of Code: Trench Map - by Thijs de Groot
"""

import numpy as np
import matplotlib.pyplot as plt

image = np.array([])
# read input
with open('input.txt', 'r', encoding='utf-8') as file:
    en_al_in = np.array(list(file.readline().strip()))
    enhancement_algorithm = np.zeros_like(en_al_in)
    enhancement_algorithm[en_al_in == '#'] = 1
    enhancement_algorithm[en_al_in == '.'] = 0
    enhancement_algorithm = enhancement_algorithm.astype(int)

    next(file)  # empty line
    for line in file:
        row_in = np.array(list(line.strip()))
        row_in_int = np.zeros_like(row_in)
        row_in_int[row_in == '#'] = 1
        row_in_int[row_in == '.'] = 0

        if image.size == 0:
            image = row_in_int.astype(int)
        else:
            image = np.vstack([image, row_in_int.astype(int)])

# to acount for 'infinity', we need to evaluate all current pixels. The scan box is 3x3,
# so we need two above and below the image
image_border_width = 2

new_image = image.copy()

number_of_cycles = 50  # = 2 for part1

for cycle_count in range(number_of_cycles):
    image = new_image.copy()
    row_size, col_size = np.shape(image)

    # set an outline around the image to simulate infinity due to the flashing 'infinity', we need to
    # switch between one and zero; the first time we set the outline, its all black dots, next time,
    # its all white pixels (ones in our case)

    fill = 0  # for filling the edges that we miss because of non-infinity matrix
    if cycle_count % 2 == 0:
        fill = 1  # fill needs to be opposite, as it is set AFTER the enhancement algorithm
        image_with_border = np.zeros([row_size + image_border_width * 2, col_size + image_border_width * 2]).astype(int)
    else:
        fill = 0
        image_with_border = np.ones([row_size + image_border_width * 2, col_size + image_border_width * 2]).astype(int)
    # insert image in infinity
    image_with_border[image_border_width:-image_border_width, image_border_width:-image_border_width] = image

    # set all at once, so not in image_with_border but in a new copy
    new_image = image_with_border.copy()

    # 'enhance' each pixel
    for row in range(1, row_size + 2 * image_border_width - 1):
        for col in range(1, col_size + 2 * image_border_width - 1):
            current_binary_array = image_with_border[row - 1:row + 2, col - 1:col + 2].flatten()
            current_binary_string = ''.join(current_binary_array.astype(str))
            enhancement_algorithm_index = int(current_binary_string, 2)
            new_image[row, col] = enhancement_algorithm[enhancement_algorithm_index]

    # account for infinity:
    new_image[0, :] = fill
    new_image[-1, :] = fill
    new_image[:, 0] = fill
    new_image[:, -1] = fill

print(f'answer: {np.sum(new_image)}')
# plt.clf()
# plt.imshow(new_image, cmap='hot')
# plt.show()
