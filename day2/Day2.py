directions = []
with open('input.txt') as file:
    for line in file:
        directions.append(line.rstrip())

depth = 0
horizontal_position = 0

for direction in directions:
    command, amount = direction.split(' ')

    if command == 'forward':
        horizontal_position += int(amount)
    elif command == 'down':
        depth += int(amount)
    elif command == 'up':
        depth -= int(amount)
    else:
        raise ValueError(f'No or wrong command found. Command: {command}')

    if depth < 0:
        raise ValueError('depth < 0 (floating above water?)')

print(f'depth: {depth}, pos: {horizontal_position}, answer 1: {depth * horizontal_position}')

# ------------------- Part 2 -----------------------

depth = 0
horizontal_position = 0
aim = 0

for direction in directions:
    command, amount = direction.split(' ')

    if command == 'forward':
        horizontal_position += int(amount)
        depth += aim * int(amount)
    elif command == 'down':
        aim += int(amount)
    elif command == 'up':
        aim -= int(amount)
    else:
        raise ValueError(f'No or wrong command found. Command: {command}')

    if depth < 0:
        raise ValueError('depth < 0 (floating above water?)')

    print(f'{command}, {amount}, new depth: {depth}, new pos: {horizontal_position}, new aim: {aim}')

print(f'depth: {depth}, pos: {horizontal_position}, answer 2: {depth * horizontal_position}')
