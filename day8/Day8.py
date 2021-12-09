import numpy as np


def split_and_sort(string_in):
    string_list = string_in.split(' ')
    sorted_string_list = [''.join(sorted(string_el)) for string_el in string_list]
    sorted_digits = np.array(sorted_string_list, dtype=str)
    return sorted_digits


count_array = np.zeros(10).astype(int)

with open('input.txt') as file:
    for line in file:
        [signal, output] = line.strip().split(' | ')
        output_digit_strings = output.split(' ')
        for digit in output_digit_strings:
            digit_len = len(digit)
            if digit_len == 2:
                count_array[1] += 1
            if digit_len == 3:
                count_array[7] += 1
            if digit_len == 4:
                count_array[4] += 1
            if digit_len == 7:
                count_array[8] += 1

print(f'answer 1: {np.sum(count_array)}')

correct_digit_array = np.zeros(10).astype(str)
total_sum = 0

with open('input.txt') as file:
    for line in file:
        [signal, output] = line.strip().split(' | ')

        sorted_signal_digits = split_and_sort(signal)
        sorted_output_digits = split_and_sort(output)

        correct_digit_array[1] = sorted_signal_digits[np.char.str_len(sorted_signal_digits) == 2][0]
        correct_digit_array[4] = sorted_signal_digits[np.char.str_len(sorted_signal_digits) == 4][0]
        correct_digit_array[7] = sorted_signal_digits[np.char.str_len(sorted_signal_digits) == 3][0]
        correct_digit_array[8] = sorted_signal_digits[np.char.str_len(sorted_signal_digits) == 7][0]

        six_bars = sorted_signal_digits[np.char.str_len(sorted_signal_digits) == 6]

        # the one with 6 bar which has all of 4 is the 9
        six_bars_matrix = np.zeros([4, 3]).astype(bool)

        for index, d_char in enumerate(correct_digit_array[4]):
            six_bars_matrix[index, :] = np.core.defchararray.find(six_bars, d_char) != -1
        correct_digit_array[9] = six_bars[np.all(six_bars_matrix, axis=0)][0]
        six_bars_remaining = six_bars[np.invert(np.all(six_bars_matrix, axis=0))]

        # the of the remaining with 6 the one which has all of 1 is 0
        six_bars_rem_matrix = np.zeros([2, 2]).astype(bool)

        for index, d_char in enumerate(correct_digit_array[1]):
            six_bars_rem_matrix[index, :] = np.core.defchararray.find(six_bars_remaining, d_char) != -1
        correct_digit_array[0] = six_bars_remaining[np.all(six_bars_rem_matrix, axis=0)][0]
        # the remaining one is 6
        correct_digit_array[6] = six_bars_remaining[np.invert(np.all(six_bars_rem_matrix, axis=0))][0]

        five_bars = sorted_signal_digits[np.char.str_len(sorted_signal_digits) == 5]

        # the one with 5 bar which has all of 7 is the 3
        five_bars_matrix = np.zeros([3, 3]).astype(bool)

        for index, d_char in enumerate(correct_digit_array[7]):
            five_bars_matrix[index, :] = np.core.defchararray.find(five_bars, d_char) != -1
        correct_digit_array[3] = five_bars[np.all(five_bars_matrix, axis=0)][0]
        five_bars_remaining = five_bars[np.invert(np.all(five_bars_matrix, axis=0))]

        # the of the remaining with 5 the one which has all of 6 is 5
        five_bars_rem_matrix = np.zeros([6, 2]).astype(bool)

        for index, d_char in enumerate(correct_digit_array[6]):
            five_bars_rem_matrix[index, :] = np.core.defchararray.find(five_bars_remaining, d_char) != -1
            
        correct_digit_array[5] = five_bars_remaining[np.sum(five_bars_rem_matrix, axis=0) == 5][0]
        # the one remaining is 2
        correct_digit_array[2] = five_bars_remaining[np.sum(five_bars_rem_matrix, axis=0) == 4][0]

        print(correct_digit_array)
        print(sorted_output_digits)
        this_sum = 0
        for index, output_digit in enumerate(sorted_output_digits):
            number_digit = np.nonzero(correct_digit_array == output_digit)[0][0]
            power = 3 - index
            this_sum += number_digit * (10 ** power)
        total_sum += this_sum

print(f'answer 2: {total_sum}')
