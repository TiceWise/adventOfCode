"""
Day 19 of Advent of Code: Beacon Scanner - by Thijs de Groot
"""

import numpy as np

scanners = {}
# read input
with open('testinput.txt', 'r', encoding='utf-8') as file:
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

matching_scanners = []
rotations = []
mirrors = []
translations = []

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

            # Part 2:
            beacons_scanner1, beacons_scanner2 = np.where(match_matrix > 1)

            bc1_xyz = scanners[scanner1_counter][beacons_scanner1[0], :]
            bc2_xyz = scanners[scanner1_counter][beacons_scanner1[1], :]
            bc3_xyz = scanners[scanner2_counter][beacons_scanner2[0], :]
            bc4_xyz = scanners[scanner2_counter][beacons_scanner2[1], :]

            dx1 = bc2_xyz[0] - bc1_xyz[0]
            dy1 = bc2_xyz[1] - bc1_xyz[1]
            dz1 = bc2_xyz[2] - bc1_xyz[2]

            dx2 = bc4_xyz[0] - bc3_xyz[0]
            dy2 = bc4_xyz[1] - bc3_xyz[1]
            dz2 = bc4_xyz[2] - bc3_xyz[2]

            rotation_matrix = [0, 0, 0]
            mirror_matrix = [0, 0, 0]

            if dx1 == dx2:
                rotation_matrix[0] = 0
                mirror_matrix[0] = 1
            if dx1 == -dx2:
                rotation_matrix[0] = 0
                mirror_matrix[0] = -1
            if dx1 == dy2:
                rotation_matrix[0] = 1
                mirror_matrix[0] = 1
            if dx1 == -dy2:
                rotation_matrix[0] = 1
                mirror_matrix[0] = -1
            if dx1 == dz2:
                rotation_matrix[0] = 2
                mirror_matrix[0] = 1
            if dx1 == -dz2:
                rotation_matrix[0] = 2
                mirror_matrix[0] = -1

            if dy1 == dx2:
                rotation_matrix[1] = 0
                mirror_matrix[1] = 1
            if dy1 == -dx2:
                rotation_matrix[1] = 0
                mirror_matrix[1] = -1
            if dy1 == dy2:
                rotation_matrix[1] = 1
                mirror_matrix[1] = 1
            if dy1 == -dy2:
                rotation_matrix[1] = 1
                mirror_matrix[1] = -1
            if dy1 == dz2:
                rotation_matrix[1] = 2
                mirror_matrix[1] = 1
            if dy1 == -dz2:
                rotation_matrix[1] = 2
                mirror_matrix[1] = -1

            if dz1 == dx2:
                rotation_matrix[2] = 0
                mirror_matrix[2] = 1
            if dz1 == -dx2:
                rotation_matrix[2] = 0
                mirror_matrix[2] = -1
            if dz1 == dy2:
                rotation_matrix[2] = 1
                mirror_matrix[2] = 1
            if dz1 == -dy2:
                rotation_matrix[2] = 1
                mirror_matrix[2] = -1
            if dz1 == dz2:
                rotation_matrix[2] = 2
                mirror_matrix[2] = 1
            if dz1 == -dz2:
                rotation_matrix[2] = 2
                mirror_matrix[2] = -1

            translation_matrix = bc3_xyz[rotation_matrix] * mirror_matrix - bc1_xyz

            matching_scanners.append([scanner1_counter, scanner2_counter])
            rotations.append(rotation_matrix)
            mirrors.append(mirror_matrix)
            translations.append(translation_matrix)

        # print(bc1_xyz)
        # print(bc2_xyz)
        # print(bc3_xyz)
        # print(bc4_xyz)
        # take one matching set of beacons of each (double check with another set maybe)
        # x may then be x, y, z, -x, -y, -z
        # y may then be those but minus the positive and negative which x is
        # one option left for z, but still might be possitive or negative
        # then we know the rotation/mirror, determine the translation, and store everything.

    unique_beacons += len(scanners[scanner1_counter]) - matches  # add the number of beacons minus the doubles (matches)

known_scanners = {0: np.array([0, 0, 0])}

unknown_scanners = list(range(1, len(scanners)))

print(known_scanners)
print(matching_scanners)
print(rotations)
print(mirrors)
print(translations)

while len(unknown_scanners) > 0:
    for index, matching in enumerate(matching_scanners):
        if matching[0] in unknown_scanners and matching[1] in known_scanners:
            known_scanners[matching[0]] = known_scanners[matching[1]] + translations[index] * mirrors[index]
            unknown_scanners.remove(matching[0])
        if matching[1] in unknown_scanners and matching[0] in known_scanners:
            known_scanners[matching[1]] = known_scanners[matching[0]] - translations[index] * mirrors[index]
            unknown_scanners.remove(matching[1])

print(known_scanners)
print(unique_beacons)
