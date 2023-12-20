import sys

A, B = sys.stdin.readline().split()

A, B = A[::-1], B[::-1]

A, B = int(A), int(B)

print(max(A, B))
