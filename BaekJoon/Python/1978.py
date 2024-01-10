import sys

N = int(sys.stdin.readline().strip())
numbers = list(map(int, sys.stdin.readline().strip().split()))

answer = 0

for i in numbers:
    yaksoo = 0
    for j in range(1, i + 1):
        if i % j == 0:
            yaksoo += 1
    if yaksoo == 2:
        answer += 1

print(answer)
