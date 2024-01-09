import sys

A, B, V = map(int, sys.stdin.readline().strip().split())

day = (V-A) // (A-B)

if V < A:
    print(1)
elif (V-A) % (A-B) == 0:
    print(day + 1)
else:
    # (V-A) % (A-B)의 결과가 0이 아닌 경우: day를 계산할 때 0.x일은 버리는 것이므로, 하루가 더 걸릴 것이다.
    print(day + 2)
