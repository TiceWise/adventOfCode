import numpy as np

size = 0
with open('input.txt') as file:
    for line in file:
        [x1y1, x2y2] = line.strip().split(' -> ')
        [x1, y1] = x1y1.split(',')
        [x2, y2] = x2y2.split(',')
        size = max(size, int(x1), int(y1), int(x2), int(y2))

field = np.zeros([size + 1, size + 1])

with open('input.txt') as file:
    for line in file:
        [x1y1, x2y2] = line.strip().split(' -> ')
        [x1, y1] = x1y1.split(',')
        [x2, y2] = x2y2.split(',')
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)

        if x1 == x2:
            y1i = min(int(y1), int(y2))
            y2i = max(int(y1), int(y2))
            print(f'x1=x2 {x1} {y1} , {x2} {y2}')
            field[y1i:y2i + 1, x1] = field[y1i:y2i + 1, x1] + 1
        if y1 == y2:
            x1i = min(int(x1), int(x2))
            x2i = max(int(x1), int(x2))
            print(f'y1=y2 {x1} {y1} , {x2} {y2}')
            field[y1, x1i:x2i + 1] = field[y1, x1i:x2i + 1] + 1

        # -------- part 2 ---------
        if (x1 < x2 and y1 < y2) or (x1 > x2 and y1 > y2):
            x1i = min(int(x1), int(x2))
            x2i = max(int(x1), int(x2))
            y1i = min(int(y1), int(y2))
            y2i = max(int(y1), int(y2))
            print(f'diag1 {x1} {y1} , {x2} {y2}')
            field[y1i:y2i + 1, x1i:x2i + 1] = field[y1i:y2i + 1, x1i:x2i + 1] + np.eye(x2i - x1i + 1)

        if (x1 < x2 and y1 > y2) or (x1 > x2 and y1 < y2):
            x1i = min(int(x1), int(x2))
            x2i = max(int(x1), int(x2))
            y1i = min(int(y1), int(y2))
            y2i = max(int(y1), int(y2))
            print(f'diag2 {x1} {y1} , {x2} {y2}')
            field[y1i:y2i + 1, x1i:x2i + 1] = field[y1i:y2i + 1, x1i:x2i + 1] + np.fliplr(np.eye(x2i - x1i + 1))

print(field)
print(f'answer1: {np.count_nonzero(field >= 2)}')
