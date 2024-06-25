import sys
from collections import deque
input = sys.stdin.readline

N, K = map(int, input().split())

queue_1 = deque(range(1, N + 1))
queue_2 = deque()

while len(queue_1) != 0:
    for _ in range(K-1):
        queue_1.append(queue_1[0])
        queue_1.popleft()
    queue_2.append(queue_1.popleft())
    
print("<", end="")
print(*queue_2, sep=", ", end="")
print(">")
