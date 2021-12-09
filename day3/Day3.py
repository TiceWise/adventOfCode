import numpy as np


def bool2int(bool_arr_in):
    bool_sum = 0
    for i, bit in enumerate(np.flip(bool_arr_in)):
        bool_sum += bit * (2 ** i)
    return bool_sum


array_from_file = np.loadtxt('input.txt', dtype=str)

arr = np.empty(shape=(len(array_from_file), len(array_from_file[0])))

for index, row in enumerate(array_from_file):
    arr[index] = np.array(list(row))

gamma_bits = (arr.sum(axis=0) > len(arr) / 2).astype(int)
epsilon_bits = (arr.sum(axis=0) < len(arr) / 2).astype(int)

gamma = bool2int(gamma_bits)
epsilon = bool2int(epsilon_bits)

print(f"gamma: {gamma}, epsilon: {epsilon} answer 1: {gamma * epsilon}")

# ------------------- Part 2 -----------------------

result_arr = arr.copy()
index = 0
while len(result_arr) > 1:
    bit_criteria = int((result_arr.sum_of_low_points(axis=0) >= len(result_arr) / 2)[index])
    result_arr = result_arr[result_arr[:, index] == bit_criteria]
    index += 1

print('-------------')
print(result_arr)
oxygen_generator_rating = bool2int(result_arr[0].astype(int))
print(oxygen_generator_rating)

result_arr = arr.copy()
index = 0
while len(result_arr) > 1:
    bit_criteria = int((result_arr.sum_of_low_points(axis=0) < len(result_arr) / 2)[index])
    result_arr = result_arr[result_arr[:, index] == bit_criteria]
    index += 1

print('-------------')
print(result_arr)
co2_scrubber_rating = bool2int(result_arr[0].astype(int))
print(co2_scrubber_rating)

print(
    f"oxygen_generator_rating: {oxygen_generator_rating}, epsilon: {co2_scrubber_rating} answer 2: {oxygen_generator_rating * co2_scrubber_rating}")
