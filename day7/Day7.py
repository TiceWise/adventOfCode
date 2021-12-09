import numpy as np

f = open('input.txt')

positions = np.array(list(f.readline().strip().split(','))).astype(int)

level_q1 = 0
min_fuel_cost_q1 = 1000000000000
level_q2 = 0
min_fuel_cost_q2 = 1000000000000

for i in range(np.max(positions)):
    distance = np.absolute(positions - i)
    fuel_cost_q1 = np.sum(distance)
    if fuel_cost_q1 < min_fuel_cost_q1:
        min_fuel_cost_q1 = fuel_cost_q1
        level_q1 = i

    fuel_cost_q2 = np.sum(distance * (distance + 1) / 2)
    print(fuel_cost_q2)
    if fuel_cost_q2 < min_fuel_cost_q2:
        min_fuel_cost_q2 = fuel_cost_q2
        level_q2 = i

print(f'answer1 : {min_fuel_cost_q1} at {level_q1}')
print(f'answer2 : {min_fuel_cost_q2} at {level_q2}')
