import sys
from collections import deque
input = sys.stdin.readline

N = int(input())

queue = deque(range(1, N + 1))

while len(queue) != 1:
    queue.popleft()
    queue.append(queue[0])
    queue.popleft()
    
print(queue[0])
