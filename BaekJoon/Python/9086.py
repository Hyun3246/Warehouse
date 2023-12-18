import sys

T = int(sys.stdin.readline())

answer = list()

for i in range(T):
    S = sys.stdin.readline().rstrip()
    answer.append(S[0] + S[-1])

for i in range(T):
    print(answer[i])
