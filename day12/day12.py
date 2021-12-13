"""
Day 12 of Advent of Code: Passage Pathing - by Thijs de Groot
"""

import numpy as np

PART1 = True
CAVES = {}
PATHS = []
PATH_COUNT = 0


class Cave:
    """
    Cave initialized with a name, is small or large, and has a list of connected caves
    """

    def __init__(self, name: str):
        self.name = name
        self.is_small = name.islower()
        self.connected_caves = []

    def add_connect_cave(self, cave_to_add: 'Cave'):
        self.connected_caves.append(cave_to_add)


def connect_caves(cave1: Cave, cave2: Cave):
    cave1.add_connect_cave(cave2)
    cave2.add_connect_cave(cave1)


def is_cave_visitable(cave: Cave, path):
    any_small_cave_visited_twice = PART1  # for part one simply set this to True
    for _, current_cave in CAVES.items():
        if current_cave.is_small and path.count(current_cave.name) > 1:
            any_small_cave_visited_twice = True

    # cave is not visitable when name is 'start'...
    # ... if we not have visited a small cave twice, we may visit a small cave for the second time
    # ... if we have visited a small cave twice, we may visit this small cave only once (part 1)
    if cave.name == 'start' or (any_small_cave_visited_twice and cave.is_small and path.count(cave.name) > 0):
        return False
    return True


def visit_caves(cave: Cave, path):
    global PATH_COUNT
    path.append(cave.name)

    if cave.name == 'end':
        PATH_COUNT += 1
        PATHS.append(','.join(path))
    else:
        for visiting_cave in cave.connected_caves:
            if is_cave_visitable(visiting_cave, path):
                visit_caves(visiting_cave, path)
    path.pop()


def main():
    global PART1

    PART1 = True

    with open('input.txt', 'r', encoding='utf-8') as file:
        for line in file:
            [cave_1_str, cave_2_str] = line.strip().split('-')
            if cave_1_str not in CAVES:
                CAVES[cave_1_str] = Cave(cave_1_str)
            if cave_2_str not in CAVES:
                CAVES[cave_2_str] = Cave(cave_2_str)
            connect_caves(CAVES[cave_1_str], CAVES[cave_2_str])

    path = []
    visit_caves(CAVES['start'], path)
    paths_array = np.asarray(PATHS)
    print(f'answer 1: {len(paths_array)}')

    PART1 = False
    path = []
    visit_caves(CAVES['start'], path)
    paths_array = np.asarray(PATHS)
    print(f'answer 2: {len(paths_array)}')


if __name__ == "__main__":
    main()
