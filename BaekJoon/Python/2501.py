import sys

N, K = map(int, sys.stdin.readline().strip().split())

numbers = []

for i in range(1, N + 1):
    if N % i == 0:
        numbers.append(i)
    if len(numbers) >= K:
        print(numbers[-1])
        break

if len(numbers) < K:
    print(0)
