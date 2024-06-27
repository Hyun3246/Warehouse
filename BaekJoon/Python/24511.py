# 큐를 따로따로 보지 말고 하나의 큐로 생각
import sys
from collections import deque
input = sys.stdin.readline

N = int(input())

A = list(map(int, input().split()))

B = list(map(int, input().split()))

M = int(input())

C = list(map(int, input().split()))

returns = []

queuestack = deque([B[i] for i in range(N) if A[i] == 0])

for i in range(M):
    queuestack.appendleft(C[i])
    returns.append(queuestack.pop())

print(*returns)
