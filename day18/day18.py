"""
Day 18 of Advent of Code: Snailfish - by Thijs de Groot
"""
import math


def reduce_once(reducing_string):
    # 'If any pair is nested inside four pairs, the leftmost such pair explodes.'
    # Check if a pair is nested in four pairs:
    # print('reducing: ' + reducing_string)
    reducing_list = list(reducing_string)
    open_pairs = 0
    exploded = False
    for char_index, char in enumerate(reducing_list):
        if char == '[':
            open_pairs += 1
            if open_pairs == 5:
                # print('explode')
                # determine current pair:
                closing_index = char_index
                find_close = reducing_list[closing_index]
                while find_close != ']':
                    closing_index += 1
                    find_close = reducing_list[closing_index]

                # determine current digits
                current_pair = ''.join(reducing_list[char_index:closing_index + 1])
                current_pair = current_pair.replace('[', '')
                current_pair = current_pair.replace(']', '')
                left_str, right_str = current_pair.split(',')
                left_num = int(left_str)
                right_num = int(right_str)

                # add left to left next digit
                left_index = char_index
                find_left = reducing_list[left_index]
                # check if there is a number to the left
                while left_index >= 0 and not find_left.isdigit():
                    left_index -= 1
                    find_left = reducing_list[left_index]

                # if there is...
                if find_left.isdigit():
                    # check if it is a double digit and add left number to that number and overwrite
                    if left_index > 0 and reducing_list[left_index - 1].isdigit():
                        find_left = ''.join(reducing_list[left_index - 1: left_index + 1])
                        reducing_list[left_index - 1:left_index + 1] = str(int(find_left) + left_num)
                    else:
                        reducing_list[left_index] = str(int(find_left) + left_num)

                # add right to right next digit
                right_index = closing_index + 1
                find_right = reducing_list[right_index]
                # check if there is a number to the right
                while right_index < len(reducing_list) - 1 and not find_right.isdigit():
                    right_index += 1
                    find_right = reducing_list[right_index]

                # if there is...
                if find_right.isdigit():
                    # check if it is a double digit and add right number to that number and overwrite
                    if right_index < len(reducing_list) - 1 and reducing_list[right_index + 1].isdigit():
                        find_right = ''.join(reducing_list[right_index: right_index + 2])
                        reducing_list[right_index: right_index + 2] = str(int(find_right) + right_num)
                    else:
                        reducing_list[right_index] = str(int(find_right) + right_num)

                # replace current pair with 0:
                reducing_list[char_index:closing_index + 1] = '0'

                exploded = True
                break
        if char == ']':
            open_pairs -= 1

    # if no pair exploded, a pair might split
    # 'If any regular number is 10 or greater, the leftmost such regular number splits.'
    if not exploded:
        for char_index, char in enumerate(reducing_list[:-1]):
            # check triple digits; the current and next two need to be digits
            if char.isdigit() and char_index < len(reducing_list) - 2 and reducing_list[char_index + 1].isdigit() and \
                    reducing_list[char_index + 2].isdigit():
                split_number = int(''.join(reducing_list[char_index:char_index + 3]))
                # replace number with splitted pair
                reducing_list[char_index:char_index + 3] = '[' + str(math.floor(split_number / 2)) + ',' + str(
                    math.ceil(split_number / 2)) + ']'

                break

            # check double digits; the current and next one need to be digits
            elif char.isdigit() and reducing_list[char_index + 1].isdigit():
                split_number = int(''.join(reducing_list[char_index:char_index + 2]))
                # replace number with splitted pair
                reducing_list[char_index:char_index + 2] = '[' + str(math.floor(split_number / 2)) + ',' + str(
                    math.ceil(split_number / 2)) + ']'

                break

    return ''.join(reducing_list)


def magnitude_once(magnitude_string):
    magnitude_list = list(magnitude_string)
    for char_index, char in enumerate(magnitude_list):
        if char == ']':
            closing_index = char_index
            # determine current pair:
            opening_index = char_index
            find_open = magnitude_list[opening_index]
            while find_open != '[':
                opening_index -= 1
                find_open = magnitude_list[opening_index]

            # determine current digits
            current_pair = ''.join(magnitude_list[opening_index:closing_index + 1])
            current_pair = current_pair.replace('[', '')
            current_pair = current_pair.replace(']', '')
            left_str, right_str = current_pair.split(',')
            left_num = int(left_str)
            right_num = int(right_str)

            magnitude_list[opening_index:closing_index + 1] = str(left_num * 3 + right_num * 2)
            return ''.join(magnitude_list)


def fully_reduce(string_to_reduce):
    prev_string = string_to_reduce
    reduced_string = reduce_once(string_to_reduce)
    while prev_string != reduced_string:
        prev_string = reduced_string
        reduced_string = reduce_once(prev_string)
    return reduced_string


def magnitude_total(string_to_magnitude):
    magnitude_total_str = magnitude_once(string_to_magnitude)
    while not magnitude_total_str.isnumeric():
        # print(magnitude_total)
        magnitude_total_str = magnitude_once(magnitude_total_str)
    return int(magnitude_total_str)


CURRENT_STRING = ''

with open('input.txt', 'r', encoding='utf-8') as file:
    for index, line in enumerate(file):
        # print(f'--- line {index} ---')
        if index == 0:
            CURRENT_STRING = line.strip()
        else:
            CURRENT_STRING = '[' + CURRENT_STRING + ',' + line.strip() + ']'

            CURRENT_STRING = fully_reduce(CURRENT_STRING)
        # print(CURRENT_STRING)

print(f'answer 1: {magnitude_total(CURRENT_STRING)}')

snail_numbers = []

with open('input.txt', 'r', encoding='utf-8') as file:
    for index, line in enumerate(file):
        snail_numbers.append(line.strip())

magnitude_max = 0

for snail_number1 in snail_numbers:
    for snail_number2 in snail_numbers:
        current_snail = '[' + snail_number1 + ',' + snail_number2 + ']'

        reduced_string = fully_reduce(current_snail)

        current_magnitude = magnitude_total(reduced_string)
        if current_magnitude > magnitude_max:
            magnitude_max = current_magnitude

print(f'answer 2: {magnitude_max}')
