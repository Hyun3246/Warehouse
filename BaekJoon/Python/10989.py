# 키워드 정렬

import sys

N = int(sys.stdin.readline().strip())

numbers = {}

for i in range(N):
    num = int(sys.stdin.readline().strip())
    if num in numbers:
        numbers[num] += 1
    else:
        numbers[num] = 1

keys = list(numbers.keys())

keys.sort()

for i in keys:
    for j in range(numbers[i]):
        print(i)
