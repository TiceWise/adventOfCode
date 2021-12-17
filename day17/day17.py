"""
Day 17 of Advent of Code: Trick Shot - by Thijs de Groot
"""

# read input
with open('input.txt', 'r', encoding='utf-8') as file:
    target_in = file.readline().strip()

left, right = target_in.split(',')
y, y_max = right.split('..')
_, y_min = y.split('=')
x, x_max = left.split('..')
_, x_min = x.split('=')

print(f'target: x: {x_min} - {x_max}, y: {y_min} - {y_max}')

x_min = int(x_min)
x_max = int(x_max)
y_min = int(y_min)
y_max = int(y_max)


def shoot(v_x, v_y, debug=False):
    # initialize starting position
    x = 0
    y = 0

    y_record = y

    while True:
        # update x and y location based on velocity
        x += v_x
        y += v_y

        # check for hit
        hit = x_min <= x <= x_max and y_min <= y <= y_max

        # check for height record
        if y > y_record:
            y_record = y

        if debug:
            print(f'x: {x}, y: {y}, v_x: {v_x}, v_y: {v_y}, in target: {hit}')

        # update horizontal velocity: increases/decreases towards 0
        if v_x > 0:
            v_x -= 1
        elif v_x < 0:
            v_x += 1

        # update vertical velocity: always decreases (gravity)
        v_y -= 1

        # if hit, return true (hit) and return the height record
        if hit:
            if debug:
                print('HIT')
            return True, y_record
        # check for overshoot (we missed)
        elif x > x_max or y < y_min:
            if debug:
                print('MISS')
            return False, -1


Y_TOTAL_RECORD = 0
HIT_COUNT = 0

# started brute force:
# v_x in range(0,500) (x must always be in direction of target, so positive)
# v_y in range(-500,500)

# a bit smarter approach; finding the mins and maxs at which we still had a valid hit
# V_X_MIN = 500
# V_X_MAX = 0
#
# V_Y_MIN = 500
# V_Y_MAX = -500

DEBUG = False

# just try many v_x and v_y combinations
for v_x in range(0, 300):
    # display a counter to get a feeling of how long this is going to take...
    if v_x % 100 == 0 and DEBUG:
        print(v_x)

    for v_y in range(-200, 200):
        current_hit, current_y_record = shoot(v_x, v_y)
        # record height record
        if current_y_record > Y_TOTAL_RECORD:
            Y_TOTAL_RECORD = current_y_record
            if DEBUG:
                print(f'new record: {Y_TOTAL_RECORD}, at v = ({v_x},{v_y})')
        # count hits
        if current_hit:
            HIT_COUNT += 1

            # determining range for big input, could be done with a lot of random values initially as start,
            # if v_x > V_X_MAX:
            #     V_X_MAX = v_x
            # if v_x < V_X_MIN:
            #     V_X_MIN = v_x
            # if v_y > V_Y_MAX:
            #     V_Y_MAX = v_y
            # if v_y < V_Y_MIN:
            #     V_Y_MIN = v_y

# print(f'x in range: {V_X_MIN} - {V_X_MAX}, y in range: {V_Y_MIN}, {V_Y_MAX}')

print(f'answer 1: {Y_TOTAL_RECORD}')
print(f'answer 2: {HIT_COUNT}')
