"""
Day 19 of Advent of Code: Beacon Scanner - by Thijs de Groot
"""

import numpy as np

scanners = {}
# read input
with open('input.txt', 'r', encoding='utf-8') as file:
    for index, line in enumerate(file):
        # read scanner number
        if line[0:3] == '---':
            _, right_part = line.strip().split(' scanner ')
            scanner_str, _ = right_part.split(' ')
            scanner_number = int(scanner_str)
            scanners[scanner_number] = np.array([])
        elif line != '\n':
            x, y, z = line.strip().split(',')
            if scanners[scanner_number].size == 0:
                scanners[scanner_number] = np.array([int(x), int(y), int(z)])
            else:
                scanners[scanner_number] = np.vstack([scanners[scanner_number], [int(x), int(y), int(z)]])

# determine unique identifiers between two scanners; sum of squared distance, min and max of abs distance
# inspired by https://www.reddit.com/r/adventofcode/comments/rjpf7f/comment/hp551kv/?utm_source=share&utm_medium=web2x&context=3
# I was trying cumbersome solutions for days so for the first time i went looking for inspiration

dis_matrixes = {}
min_matrixes = {}
max_matrixes = {}

for (scanner_number, scanner) in scanners.items():
    number_of_beacons_tup = np.shape(scanner)
    number_of_beacons = number_of_beacons_tup[0]
    dis_matrix = np.zeros([number_of_beacons, number_of_beacons]).astype(int)
    min_matrix = np.zeros([number_of_beacons, number_of_beacons]).astype(int)
    max_matrix = np.zeros([number_of_beacons, number_of_beacons]).astype(int)
    for i, beacon1 in enumerate(scanner):
        for j, beacon2 in enumerate(scanner):
            dx = abs(beacon1[0] - beacon2[0])
            dy = abs(beacon1[1] - beacon2[1])
            dz = abs(beacon1[2] - beacon2[2])
            dis_matrix[i, j] = dx * dx + dy * dy + dz * dz
            min_matrix[i, j] = min(dx, dy, dz)
            max_matrix[i, j] = max(dx, dy, dz)

    dis_matrixes[scanner_number] = dis_matrix.astype(int)
    min_matrixes[scanner_number] = min_matrix.astype(int)
    max_matrixes[scanner_number] = max_matrix.astype(int)

unique_beacons = 0

for scanner1_counter in scanners:
    matches = 0
    for scanner2_counter in range(scanner1_counter + 1, len(scanners)):
        # print(f'matching scanner {scanner1_counter} with {scanner2_counter}')

        match_matrix = np.zeros([len(scanners[scanner1_counter]), len(scanners[scanner2_counter])]).astype(int)
        # bc = beacon counter, we're tracking 4 different; matching 1 and 2 of scanner one and 3 and 4 of scanner 2
        for bc1 in range(len(scanners[scanner1_counter])):
            for bc2 in range(bc1 + 1, len(scanners[scanner1_counter])):
                for bc3 in range(len(scanners[scanner2_counter])):
                    for bc4 in range(bc3 + 1, len(scanners[scanner2_counter])):
                        match_dis = dis_matrixes[scanner1_counter][bc1, bc2] == dis_matrixes[scanner2_counter][bc3, bc4]
                        match_min = min_matrixes[scanner1_counter][bc1, bc2] == min_matrixes[scanner2_counter][bc3, bc4]
                        match_max = max_matrixes[scanner1_counter][bc1, bc2] == max_matrixes[scanner2_counter][bc3, bc4]
                        if match_dis and match_min and match_max:
                            match_matrix[bc1, bc3] += 1
                            match_matrix[bc1, bc4] += 1
                            match_matrix[bc2, bc3] += 1
                            match_matrix[bc2, bc4] += 1

        matching_beacons_count = np.count_nonzero(match_matrix > 1)

        if matching_beacons_count > 11:
            print(f'{scanner1_counter} matches {scanner2_counter} on {matching_beacons_count} beacons')
            matches += matching_beacons_count  # count the number of matches, we can substract these from the unique count

    unique_beacons += len(scanners[scanner1_counter]) - matches  # add the number of beacons minus the doubles (matches)

print(unique_beacons)
