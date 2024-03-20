import sys

N, M = map(int, sys.stdin.readline().strip().split())
cards = list(map(int, sys.stdin.readline().strip().split()))

sums = set()

for i in cards:
    for j in cards:
        for k in cards:
            if i != j and j != k and i != k:
                sum = i + j + k
                sums.add(sum)

sums = list(sums)
sums.sort()

max_score = 0

for sum in sums:
    if sum <= M and sum > max_score:
        max_score = sum

print(max_score)
