import sys

S = sys.stdin.readline().strip()

answer = 1

for i in range(len(S)//2):
    if S[i] != S[-i-1]:
        answer = 0
        break

print(answer)
