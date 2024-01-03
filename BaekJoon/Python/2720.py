import sys

T = int(sys.stdin.readline().strip())

for i in range(T):
    C = int(sys.stdin.readline().strip())
    Q = C // 25
    C -= Q * 25

    D = C // 10
    C -= D * 10

    N = C // 5
    C -= N * 5

    P = C // 1

    print(Q, D, N, P)
