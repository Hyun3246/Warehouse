import sys

N = int(sys.stdin.readline().strip())

bags = N

for i in range(N):
    for j in range(N):
        if (i*3 + j*5) == N:
            if i + j < bags:
                bags = i + j

if bags == N:
    print(-1)
else:
    print(bags)
