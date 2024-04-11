import sys

N = int(sys.stdin.readline().strip())

numbers = []

for i in range(N):
    num = int(sys.stdin.readline().strip())
    numbers.append(num)

numbers.sort()

for i in numbers:
    print(i)
