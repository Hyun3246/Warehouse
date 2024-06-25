import sys
from collections import deque
input = sys.stdin.readline

N = int(input())
queue = deque(range(2, N + 1))

paper = list(map(int, input().split()))

order = [1]

for i in range(N-1):
    if paper[order[-1]-1] >= 0:
        for _ in range(paper[order[-1]-1]-1):
            queue.append(queue[0])
            queue.popleft()
        order.append(queue[0])
        queue.popleft()
    else:
        for _ in range(abs(paper[order[-1]-1])):
            queue.appendleft(queue[-1])
            queue.pop()
        order.append(queue[0])
        queue.popleft()

print(*order)
