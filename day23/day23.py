"""
Day 23 of Advent of Code: Amphipod - by Thijs de Groot
"""

# https://towardsdatascience.com/create-your-own-board-game-with-powerful-ai-from-scratch-part-1-5dcb028002b8

# Energy counter
# Amphipods (with energy cost per move)
# Valid positions
# Valid moves
# Goal: get in the right box

# initial game state, from input () -> Initial State
# actions: move Function (State) -> list of actions
# determine all valid moves
# result of move: new state Function (state, action) -> new state

# terminal test: check for game end: Function (state) --> True or False (amphipods in correct position)
import copy
import random
import sys

import numpy as np


def get_valid_moves_amphipod(map, amphipod, rowcol, cost_so_far):
    global valid_moves_amphipod  # tried everything to do this without global, but a flat list with multiple branches recursion.. just couldnt work it ou
    row = rowcol[0]
    col = rowcol[1]
    moves = [(-1, 0), (+1, 0), (0, -1), (0, +1)]

    map[row, col] = 'v'  # make sure we don't check this spot again
    cost_so_far += amphipod.energy_cost

    valid_list = []

    for move in moves:
        cur_row = row + move[0]
        cur_col = col + move[1]
        if map[cur_row, cur_col] == '.':
            # Amphipods will never stop on the space immediately outside any room.
            # if row = 1 and col is 3, 5, 7 or 9, it's not a valid move, but continue adding to the list
            if cur_row == 1 and (cur_col == 3 or cur_col == 5 or cur_col == 7 or cur_col == 9):
                valid_list.append([cur_row, cur_col])
            # Amphipods will never move from the hallway into a room unless that room is their destination room and that
            # room contains no amphipods which do not also have that room as their own destination.
            elif cur_row == 2:
                # only append if in target col, if bottom spot empty we must move there, otherwise we can
                # only move here if the bottom one is the brother amphipod
                if cur_col == amphipod.target_col:
                    # we must go one place lower otherwise we block the door, but that will come in the next recursive
                    if map[3, cur_col] == '.':
                        valid_list.append([cur_row, cur_col])
                    elif map[3, cur_col] == amphipod.name[0]:
                        valid_moves_amphipod.append(Move(amphipod, cur_row, cur_col, cost_so_far))
                        # we can't go any lower so no use in appending to valid_list
                else:
                    # we are in a wrong collumn, so explore next row 2
                    valid_list.append([cur_row, cur_col])
            elif cur_row == 3:
                if cur_col == amphipod.target_col:
                    valid_moves_amphipod.append(Move(amphipod, cur_row, cur_col, cost_so_far))
                    # we can't go any lower so no use in appending to valid_list
            else:
                valid_moves_amphipod.append(Move(amphipod, cur_row, cur_col, cost_so_far))
                valid_list.append([cur_row, cur_col])

    for rowcolcomb in valid_list:
        get_valid_moves_amphipod(map, amphipod, rowcolcomb, cost_so_far)


class Move:
    def __init__(self, amphipod, dest_row, dest_col, cost):
        self.amphipod = amphipod
        self.dest_row = dest_row
        self.dest_col = dest_col
        self.cost = cost

    def __repr__(self):
        return f'move: {self.amphipod.name} to {self.dest_row},{self.dest_col} at cost: {self.cost}'


class Amphipod:
    def __init__(self, name, row, col):
        self.name = name
        self.row = row
        self.col = col
        if name[0] == 'A':
            self.energy_cost = 1
            self.target_col = 3
        elif name[0] == 'B':
            self.energy_cost = 10
            self.target_col = 5
        elif name[0] == 'C':
            self.energy_cost = 100
            self.target_col = 7
        else:
            self.energy_cost = 1000
            self.target_col = 9

    def __repr__(self):
        return self.name

    def move_to(self, row, col):
        self.row = row
        self.col = col


def is_game_locked(move_list):
    if not move_list:
        return True
    else:
        return False


class State:
    def __init__(self):
        self.empty_map = np.full([5, 13], ['#'], dtype=str)
        self.empty_map[1, 1:-1] = '.'
        self.empty_map[1:-1, 3] = '.'
        self.empty_map[1:-1, 5] = '.'
        self.empty_map[1:-1, 7] = '.'
        self.empty_map[1:-1, 9] = '.'

        self.map = self.empty_map
        self.total_cost = 0

        self.amphipod_set = {}

    def initial_state_test(self):
        self.amphipod_set['A1'] = Amphipod('A1', 3, 3)
        self.amphipod_set['A2'] = Amphipod('A2', 3, 9)
        self.amphipod_set['B1'] = Amphipod('B1', 2, 3)
        self.amphipod_set['B2'] = Amphipod('B2', 2, 7)
        self.amphipod_set['C1'] = Amphipod('C1', 2, 5)
        self.amphipod_set['C2'] = Amphipod('C2', 3, 7)
        self.amphipod_set['D1'] = Amphipod('D1', 3, 5)
        self.amphipod_set['D2'] = Amphipod('D2', 2, 9)

        self.update_map()

    def initial_state(self):
        self.amphipod_set['A1'] = Amphipod('A1', 3, 5)
        self.amphipod_set['A2'] = Amphipod('A2', 3, 9)
        self.amphipod_set['B1'] = Amphipod('B1', 2, 7)
        self.amphipod_set['B2'] = Amphipod('B2', 3, 7)
        self.amphipod_set['C1'] = Amphipod('C1', 2, 3)
        self.amphipod_set['C2'] = Amphipod('C2', 2, 5)
        self.amphipod_set['D1'] = Amphipod('D1', 3, 3)
        self.amphipod_set['D2'] = Amphipod('D2', 2, 9)

        self.update_map()

    def update_map(self):
        updated_map = self.empty_map.copy()
        for name, amphipod in self.amphipod_set.items():
            updated_map[amphipod.row, amphipod.col] = name[0]
        self.map = updated_map

    def __repr__(self):
        self.update_map()
        output = ''
        for row in self.map:
            output = output + ''.join(row) + '\n'
        return output

    def get_valid_moves(self):
        global valid_moves_amphipod
        all_valid_moves = []
        for name, amphipod in self.amphipod_set.items():
            valid_moves_amphipod = []
            get_valid_moves_amphipod(self.map.copy(), amphipod, [amphipod.row, amphipod.col], 0)

            if amphipod.row == 1:
                # Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room.
                # filter list for target row:
                valid_moves_amphipod = [move_amphipod for move_amphipod in valid_moves_amphipod if
                                        move_amphipod.dest_col == amphipod.target_col]
            if amphipod.row == 2 and amphipod.col == amphipod.target_col:
                # it won't leave the room if it's good
                if self.map[amphipod.row + 1, amphipod.col] == amphipod.name[0]:
                    valid_moves_amphipod = []

            all_valid_moves.extend(valid_moves_amphipod)
        return all_valid_moves

    def do_move(self, move):
        self.amphipod_set[move.amphipod.name].move_to(move.dest_row, move.dest_col)
        self.total_cost += move.cost
        self.update_map()

    def is_game_solved(self):
        solved = True
        for name, amphipod in self.amphipod_set.items():
            if amphipod.col != amphipod.target_col:
                solved = False
        return solved


valid_moves_amphipod = []

min_score = 30000
turn_count = 0


def do_turn(state):
    global turn_count
    global min_score
    turn_count += 1
    if turn_count % 10000 == 0:
        print(f'{turn_count} turns evaluated')
    possible_moves = state.get_valid_moves()

    if not is_game_locked(possible_moves):
        for move in random.sample(possible_moves, len(possible_moves)):
            new_state = copy.deepcopy(state)
            new_state.do_move(move)
            if new_state.is_game_solved():
                current_score = new_state.total_cost
                if current_score < min_score:
                    print(f'new lowest energy: {current_score}')
                    min_score = current_score
            elif new_state.total_cost < min_score:
                do_turn(new_state)


def main():
    state = State()

    state.initial_state()

    do_turn(copy.deepcopy(state))
    print('answer 1: ', end='')
    print(min_score)


if __name__ == "__main__":
    main()
