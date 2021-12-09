import numpy as np
import time

start = time.perf_counter()
f = open('input.txt')

state = np.array(list(f.readline().strip().split(','))).astype(int)

new_count_array = np.zeros(9).astype(dtype=object)

for i in range(9):
    new_count_array[i] = np.count_nonzero(state == i)

cycles = 256  # 2 ** 64

for i in range(1, cycles + 1):
    new_count_array = np.roll(new_count_array, -1)
    new_count_array[6] = new_count_array[6] + new_count_array[8]

    if i % 1000000 == 0:
        print(f'{i} in {time.perf_counter() - start}')

end = time.perf_counter()
print(f'answer 2: {np.sum(new_count_array)} in {(end - start):.9f}s')
