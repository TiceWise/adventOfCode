depths = []
with open('day1/input.txt') as file:
    for line in file:
        depths.append(int(line.rstrip()))

count = 0
for index, depth in enumerate(depths):
    if index != 0:
        if depth > depths[index - 1]:
            count += 1

print(f"answer 1: {count}")

sumCount = 0
prevSum = 10000000000
for index, depth in enumerate(depths[:-2]):
    curSum = depths[index] + depths[index + 1] + depths[index + 2]
    print(curSum, end='')
    if curSum > prevSum:
        sumCount += 1
        print(" I", end='')
    prevSum = curSum
    print()
    
print(f"answer 2: {sumCount}")
