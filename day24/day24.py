"""
Day 24 of Advent of Code: Arithmetic Logic Unit - by Thijs de Groot
"""
import math
from random import random


# import numpy as np


def get_rand_non_zero_int():
    rand_int = 0
    while rand_int == 0:
        rand_int = math.trunc(random() * 10)
    return rand_int


# def get_rand_around(input):
#     rand_int = 0
#     while rand_int < 1 or rand_int > 9:
#         rand_int = math.trunc(np.random.normal(loc=int(input), scale=2))
#     return rand_int


var_set = {}
var_set['w'] = 0
var_set['x'] = 0
var_set['y'] = 0
var_set['z'] = 2

lowest_z = 1000000
low_zs = []
low_inputs = []

# int_start = '9' * 14

# int_start = []
# for _ in range(14):
#     int_start.append(str(get_rand_non_zero_int()))
# int_start = ''.join(int_start)

# brute force, change different integers using 10 ** x, and try random numbers every now and then. Set int_start
# to the highest (part 1) or lowest (part 2) known so far
int_start = '11815671117121'
decrease_count = 1

started = False
while int(int_start) > 111111111111:
    # while True:
    var_set = {}
    var_set['w'] = 0
    var_set['x'] = 0
    var_set['y'] = 0
    var_set['z'] = 0

    # int_as_int = int(
    #     int_start) - decrease_count * 1000000 * get_rand_non_zero_int() - decrease_count * 100 * get_rand_non_zero_int() - decrease_count * get_rand_non_zero_int()  # + get_rand_non_zero_int()  # * 10 ** 7 + 101 * decrease_count  # + 10 ** 3 + decrease_count * 1 ** 1

    int_as_int = int(
        int_start) - 1000 * decrease_count - get_rand_non_zero_int() * decrease_count
    decrease_count += 1

    input = str(int_as_int)

    if '0' in input:
        continue

    index = 0

    with open('input.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            # print(line + ': ', end='')
            if line.startswith('inp'):
                _, variable = line.split(' ')
                var_set[variable] = int(input[index])
                index += 1
                # print(f'inp: {variable} set to {var_set[variable]}')
            else:
                action, var1, var2 = line.split(' ')
                if action == 'add':
                    if var2.isalpha():
                        var_set[var1] += var_set[var2]
                    else:
                        var_set[var1] += int(var2)
                    # print(f'add: {var1} set to {var_set[var1]}')
                if action == 'mul':
                    if var2.isalpha():
                        var_set[var1] *= var_set[var2]
                    else:
                        var_set[var1] *= int(var2)
                    # print(f'mul: {var1} set to {var_set[var1]}')
                if action == 'div':
                    if var2.isalpha():
                        div_result = var_set[var1] / var_set[var2]
                        var_set[var1] = math.trunc(div_result)
                    else:
                        div_result = var_set[var1] / int(var2)
                        var_set[var1] = math.trunc(div_result)
                    # print(f'div: {var1} set to {var_set[var1]}')
                if action == 'mod':
                    if var2.isalpha():
                        var_set[var1] %= var_set[var2]
                    else:
                        var_set[var1] %= int(var2)
                    # print(f'mod: {var1} set to {var_set[var1]}')
                if action == 'eql':
                    if var2.isalpha():
                        if var_set[var1] == var_set[var2]:
                            var_set[var1] = 1
                        else:
                            var_set[var1] = 0
                    else:
                        if var_set[var1] == int(var2):
                            var_set[var1] = 1
                        else:
                            var_set[var1] = 0
                    # print(f'eql: {var1} set to {var_set[var1]}')
    if var_set['z'] <= lowest_z:
        print(f'{input}: ', end='')
        print(var_set)
        lowest_z = var_set['z']
        low_zs.append(lowest_z)
        low_inputs.append(input)
        if lowest_z == 0:
            break

print(f'{input}: ', end='')
print(var_set)
