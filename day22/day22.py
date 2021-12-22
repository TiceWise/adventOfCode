"""
Day 22 of Advent of Code: Reactor Reboot - by Thijs de Groot
"""

import numpy as np

toggles = np.array([]).astype(str)
xstarts = np.array([]).astype(int)
xends = np.array([]).astype(int)
ystarts = np.array([]).astype(int)
yends = np.array([]).astype(int)
zstarts = np.array([]).astype(int)
zends = np.array([]).astype(int)

with open('input.txt', 'r', encoding='utf-8') as file:
    for index, line in enumerate(file):
        if index == 20:
            break
        toggle, xyz_str = line.strip().split(' ')
        toggles = np.append(toggles, toggle)

        x_str, y_str, z_str = xyz_str.split(',')

        _, x_start_end = x_str.split('=')
        _, y_start_end = y_str.split('=')
        _, z_start_end = z_str.split('=')

        xstart, xend = x_start_end.split('..')
        ystart, yend = y_start_end.split('..')
        zstart, zend = z_start_end.split('..')

        xstarts = np.append(xstarts, int(xstart))
        ystarts = np.append(ystarts, int(ystart))
        zstarts = np.append(zstarts, int(zstart))

        xends = np.append(xends, int(xend))
        yends = np.append(yends, int(yend))
        zends = np.append(zends, int(zend))

# xshift yshift zshift
xshift = -np.min(xstarts)
yshift = -np.min(ystarts)
zshift = -np.min(zstarts)

xstarts = xstarts + xshift
ystarts = ystarts + yshift
zstarts = zstarts + zshift

xends = xends + xshift
yends = yends + yshift
zends = zends + zshift
print(toggles)
print(xstarts)
print(zends)

cube_map = np.zeros([np.max(xends) + 1, np.max(yends) + 1, np.max(zends) + 1], dtype=bool)

for index, toggle in enumerate(toggles):
    on_or_off = True if toggle == 'on' else False

    cube_map[xstarts[index]:xends[index] + 1, ystarts[index]:yends[index] + 1,
    zstarts[index]:zends[index] + 1] = on_or_off

answer = np.sum(cube_map)
print(answer)
