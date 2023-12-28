import sys

N, M = map(int, sys.stdin.readline().strip().split())

A, B = [], []

for i in range(N):
    row = list(map(int, sys.stdin.readline().strip().split()))
    A.append(row)

for i in range(N):
    row = list(map(int, sys.stdin.readline().strip().split()))
    B.append(row)

for i in range(N):
    for j in range(M):
        print(A[i][j] + B[i][j], end=" ")
    print()
