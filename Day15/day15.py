"""
Day 15 of Advent of Code: Chiton - by Thijs de Groot
"""

import numpy as np
import matplotlib.pyplot as plt

# from matplotlib.animation import FFMpegWriter

# read input
array = []
with open('input.txt', 'r', encoding='utf-8') as file:
    for line in file:
        array.append(list(line.strip()))
map1 = np.array(array).astype(int)

map_row = map1
temp_map = map1.copy()

# create large map
for i in range(1, 5):
    temp_map += 1
    temp_map[temp_map > 9] = 1
    map_row = np.hstack([map_row, temp_map])

map2 = map_row
temp_map = map_row.copy()

for j in range(1, 5):
    temp_map += 1
    temp_map[temp_map > 9] = 1
    map2 = np.vstack([map2, temp_map])

# map1 for part 1, map2 for part 2
map = map2

# For the movie
# metadata = dict(title='AoC Day 15', artist='Thijs de Groot')
# writer = FFMpegWriter(fps=15, metadata=metadata)
# fig = plt.figure(figsize=(12, 9))

# applying Dijkstra's algorithm (https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
visited = np.zeros_like(map).astype(bool)
tentative_distance = np.ones_like(map) * np.inf
tentative_distance[0, 0] = 0  # starting node

total_rows, total_cols = np.shape(map)

# with writer.saving(fig, "writer_test.mp4", 100):
while True:
    # for all lowest non visited node(s) (we call these the current nodes)
    current_nodes = np.nonzero(tentative_distance == np.min(tentative_distance[np.invert(visited)]))
    list_of_current_nodes = list(zip(current_nodes[0], current_nodes[1]))

    for current_node in list_of_current_nodes:
        current_row, current_col = current_node
        current_tentative_distance = tentative_distance[current_row, current_col]
        # determine neighbours: up, down, left, right
        # consider all unvisited neighbours...
        for neighbour in [(current_row - 1, current_col), (current_row + 1, current_col),
                          (current_row, current_col - 1), (current_row, current_col + 1)]:
            row, col = neighbour
            if 0 <= row < total_rows and 0 <= col < total_cols:
                if not visited[row, col]:
                    # ...and calculate their tentative distance through the current node
                    temp_distance = current_tentative_distance + map[row, col]
                    # compare the calculated tentative distance with the existing value and assign the smaller one
                    tentative_distance[row, col] = min(temp_distance, tentative_distance[row, col])
        # set current node as visited
        visited[current_row, current_col] = True

    # for movie
    # plt.clf()
    # plt.imshow(tentative_distance, cmap='viridis')
    # plt.title('distance map to starting point (top left)')
    # plt.colorbar()
    # plt.show()
    # writer.grab_frame()

    # as soon as we reach the end point, we can stop
    if visited[-1, -1]:
        # for single end plot
        # plt.clf()
        # plt.imshow(tentative_distance, cmap='viridis')
        # plt.title('distance map to starting point (top right)')
        # plt.colorbar()
        # plt.show()

        print(f'answer: {tentative_distance[-1, -1]}')
        break

# ------------- back track path (not necessary, just for movie) -----------

# initialize route map
route_map = np.zeros_like(map)

# start at right bottom
next_row = total_rows - 1
next_col = total_cols - 1

while True:
    current_row = next_row
    current_col = next_col
    # track location in route map
    route_map[current_row, current_col] = 1

    # end condition; we're at the starting point
    if current_row == 0 and current_col == 0:
        tentative_distance[route_map == 1] = 0
        # for final frame or just to plot
        # plt.clf()
        # plt.imshow(tentative_distance, cmap='viridis')
        # plt.title('distance map to starting point (top left)')
        # plt.colorbar()
        # plt.show()
        # writer.grab_frame()
        break

    # next node is the lowest node around
    lowest_neighbour = np.inf
    for neighbour in [(current_row - 1, current_col), (current_row + 1, current_col),
                      (current_row, current_col - 1), (current_row, current_col + 1)]:
        row, col = neighbour
        if 0 <= row < total_rows and 0 <= col < total_cols:
            if tentative_distance[row, col] < lowest_neighbour:
                lowest_neighbour = tentative_distance[row, col]
                # set next point
                next_row = row
                next_col = col
