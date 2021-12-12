"""
Day 12 of Advent of Code: Passage Pathing - by Thijs de Groot
"""


class Cave:
    """
    Cave initialized with a name, is small or large, small can be visited once,
    and has a list of connected caves
    """

    def __init__(self, name: str):
        self.name = name
        self.is_small = name.islower()
        self.visit_count = 0
        self.connect_caves = []
        self.visitable = True

    def add_visit(self):
        self.visit_count += 1
        if self.is_small:
            self.visitable = False

    def add_connect_cave(self, cave_to_add: 'Cave'):
        self.connect_caves.append(cave_to_add)

    def reset_visits(self):
        self.visitable = True
        self.visit_count = 0


def connect_caves(cave1: Cave, cave2: Cave):
    cave1.add_connect_cave(cave2)
    cave2.add_connect_cave(cave1)


caves = {}
PATH_COUNT = 0

with open('input.txt', 'r', encoding='utf-8') as file:
    for line in file:
        [cave_1_str, cave_2_str] = line.strip().split('-')
        print(f"{cave_1_str}-{cave_2_str}")
        if cave_1_str not in caves:
            caves[cave_1_str] = Cave(cave_1_str)
        if cave_2_str not in caves:
            caves[cave_2_str] = Cave(cave_2_str)
        connect_caves(caves[cave_1_str], caves[cave_2_str])


def visit_caves(cave: Cave, path):
    global PATH_COUNT
    cave.add_visit()
    path.append(cave.name)

    if cave.name == 'end':
        print(path)
        PATH_COUNT += 1
    else:
        for visiting_cave in cave.connect_caves:
            if visiting_cave.visitable:
                visit_caves(visiting_cave, path)
    path.pop()
    cave.reset_visits()


path = []

visit_caves(caves['start'], path)

print(PATH_COUNT)
