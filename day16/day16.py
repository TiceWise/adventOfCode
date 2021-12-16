"""
Day 16 of Advent of Code: Packet Decoder - by Thijs de Groot
"""

import numpy as np


def bit_array_to_int(bit_array):
    return int(''.join(bit_array), 2)


with open('microtestinput3.txt', 'r', encoding='utf-8') as file:
    message = list(file.readline().strip())

print(''.join(message))

total_bit_array = []

for char in message:
    # print(format(int(char, 16), '04b'))
    total_bit_array.extend(list(format(int(char, 16), '04b')))

print(''.join(total_bit_array))


def decoder(current_bit_array):
    global VERSION_SUM
    cur_bit_ar_str = ''.join(current_bit_array)
    print(f'current bit array: {cur_bit_ar_str}')
    version = bit_array_to_int(current_bit_array[:3])
    type_id = bit_array_to_int(current_bit_array[3:6])

    VERSION_SUM += version
    lit_op_str = 'literal' if type_id == 4 else 'operator'
    print(f'version: {version}, type ID: {type_id}, {lit_op_str}')
    # check for literal value
    if type_id == 4:
        should_continue = True
        current_literal_bit_array = []
        bit_tracker = 6
        while should_continue:
            # no length type id
            # next 5 are
            should_continue = bool(int(current_bit_array[bit_tracker]))
            # print(should_continue)
            current_literal_bit_array.extend(current_bit_array[bit_tracker + 1:bit_tracker + 5])
            # print(current_bit_array)
            bit_tracker += 5

        # if we're done, and all remaining bit's are zero, we're done, otherwise we continue with the next
        print(f'current literal: {bit_array_to_int(current_literal_bit_array)}')
        if not np.any(np.array(current_bit_array[bit_tracker:]).astype(int).astype(bool)):
            return
        else:
            decoder(current_bit_array[bit_tracker:])

    # else: operator
    else:
        # next bit is length type id:
        length_type_id = bool(int(current_bit_array[6]))
        if not length_type_id:
            total_length_in_bits = bit_array_to_int(current_bit_array[7:7 + 15])
            print(f'decoding {total_length_in_bits} bits')
            decoder(current_bit_array[7 + 15:7 + 15 + total_length_in_bits])
        else:
            number_of_sub_packets = bit_array_to_int(current_bit_array[7:7 + 11])
            print(f'decoding {number_of_sub_packets} packets')
            decoder(current_bit_array[7 + 11:])
            # TODO: go n times with the remainder of bit array
            # use global bit tracker?


VERSION_SUM = 0
decoder(total_bit_array)
print(f'answer: {VERSION_SUM}')
