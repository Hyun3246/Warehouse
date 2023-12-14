import sys

N, M = map(int, input().split())
boxes = [0] * N


for a in range(M):
    i, j, k = map(int, sys.stdin.readline().split())
    for b in range(i, j + 1):
        boxes[b-1] = k

for c in boxes:
    print(c, end=" ")
