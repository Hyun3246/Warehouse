import sys

N, M = map(int, sys.stdin.readline().split())

baskets = list(range(1, N + 1))

for k in range(M):
    i, j = map(int, sys.stdin.readline().split())
    baskets[i-1:j] = reversed(baskets[i-1:j])
    
for l in baskets:
    print(l, end=" ")
