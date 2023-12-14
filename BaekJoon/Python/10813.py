import sys

N, M = map(int, sys.stdin.readline().split())
boxes = list(range(1, N+1))


for a in range(M):
    i, j = map(int, sys.stdin.readline().split())
    boxes[i-1], boxes[j-1] = boxes[j-1], boxes[i-1]

for c in boxes:
    print(c, end=" ")
