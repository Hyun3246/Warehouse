import sys

M = int(sys.stdin.readline().strip())
N = int(sys.stdin.readline().strip())

prime_numbers = []

for i in range(M, N + 1):
    num_divisor = 0
    for j in range(1, i + 1):
        if i % j == 0:
            num_divisor += 1
    if num_divisor == 2:
        prime_numbers.append(i)

if len(prime_numbers) != 0:
    print(sum(prime_numbers))
    print(min(prime_numbers))
else:
    print(-1)
