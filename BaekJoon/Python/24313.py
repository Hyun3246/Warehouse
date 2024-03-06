import sys

a_1, a_0 = map(int, sys.stdin.readline().strip().split())
c = int(sys.stdin.readline().strip())
n_0 = int(sys.stdin.readline().strip())

if (a_1 * n_0 + a_0 <= c * n_0) and (a_1 <= c):
    print(1)
else:
    print(0)
