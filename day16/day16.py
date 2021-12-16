"""
Day 16 of Advent of Code: Packet Decoder - by Thijs de Groot
"""
import math


def bit_array_to_int(bit_array):
    return int(''.join(bit_array), 2)


def decoder():
    global VERSION_SUM
    global BIT_TRACKER

    v_t_width = 3
    # the next three bits are the version
    version = bit_array_to_int(TOTAL_BIT_ARRAY[BIT_TRACKER:BIT_TRACKER + v_t_width])
    BIT_TRACKER += v_t_width
    VERSION_SUM += version

    # the next three bits are the type
    type_id = bit_array_to_int(TOTAL_BIT_ARRAY[BIT_TRACKER:BIT_TRACKER + v_t_width])
    BIT_TRACKER += v_t_width

    # for debugging print:
    # lit_op_str = 'literal' if type_id == 4 else 'operator'
    # print(f'version: {version}, type ID: {type_id}, {lit_op_str}')

    # handle for literal value
    if type_id == 4:
        # initialize empty literal bit array
        literal_bit_array = []
        # always read first literal bit
        should_continue = True

        literal_width = 4
        while should_continue:
            # the next bit determines if this is the last literal bit
            should_continue = bool(int(TOTAL_BIT_ARRAY[BIT_TRACKER]))
            BIT_TRACKER += 1

            # push next four bits onto the literal bit array
            literal_bit_array.extend(TOTAL_BIT_ARRAY[BIT_TRACKER:BIT_TRACKER + literal_width])
            BIT_TRACKER += literal_width

        # for debuggin print:
        # print(f'current literal: {bit_array_to_int(literal_bit_array)}')

        # return the decoded literal
        return bit_array_to_int(literal_bit_array)

    # handle operators
    else:
        # next bit is length type id:
        length_type_id = bool(int(TOTAL_BIT_ARRAY[BIT_TRACKER]))
        BIT_TRACKER += 1

        # initialize a stack for all the literals of the current operator
        literal_stack = []
        if not length_type_id:
            length_width = 15
            # the next 15 bits are the length for the current operator
            total_length_in_bits = bit_array_to_int(TOTAL_BIT_ARRAY[BIT_TRACKER:BIT_TRACKER + length_width])
            BIT_TRACKER += length_width

            # for debugging:
            # print(f'decoding {total_length_in_bits} bits')

            # while the bit tracker is within the length of the current operator
            STOP_TRACKER = BIT_TRACKER + total_length_in_bits
            while BIT_TRACKER < STOP_TRACKER:
                # add the result to the literal stack
                literal_stack.append(decoder())
        else:
            number_width = 11
            # the next 11 bits are the number of sub packets in this operator
            number_of_sub_packets = bit_array_to_int(TOTAL_BIT_ARRAY[BIT_TRACKER:BIT_TRACKER + number_width])
            BIT_TRACKER += number_width

            # handle the defined number of sub packets
            for _ in range(number_of_sub_packets):
                # for debugging print:
                # print(f'decoding {i} of {number_of_sub_packets} packets')

                # add the result to the literal stack
                literal_stack.append(decoder())

        # if we have determined the sub packet results, apply the operator
        if type_id == 0:
            return sum(literal_stack)
        elif type_id == 1:
            return math.prod(literal_stack)
        elif type_id == 2:
            return min(literal_stack)
        elif type_id == 3:
            return max(literal_stack)
        elif type_id == 5:
            return 1 if literal_stack[0] > literal_stack[1] else 0
        elif type_id == 6:
            return 1 if literal_stack[0] < literal_stack[1] else 0
        elif type_id == 7:
            return 1 if literal_stack[0] == literal_stack[1] else 0


TOTAL_BIT_ARRAY = []
VERSION_SUM = 0
BIT_TRACKER = 0


def main():
    global TOTAL_BIT_ARRAY
    global VERSION_SUM
    global BIT_TRACKER

    with open('input.txt', 'r', encoding='utf-8') as file:
        message = list(file.readline().strip())

    for char in message:
        TOTAL_BIT_ARRAY.extend(list(format(int(char, 16), '04b')))

    # print(''.join(message))
    # print(''.join(TOTAL_BIT_ARRAY))

    value = decoder()
    print(f'answer 1: {VERSION_SUM}')
    print(f'answer 2: {value}')


if __name__ == "__main__":
    main()
