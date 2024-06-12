import sys
from collections import deque
input = sys.stdin.readline

def pop(queue):
    if len(queue) == 0:
        print(-1)
    else:
        print(queue[0])
        queue.popleft()

def empty(queue):
    if len(queue) == 0:
        print(1)
    else:
        print(0)

def front(queue):
    if len(queue) == 0:
        print(-1)
    else:
        print(queue[0])

def back(queue):
    if len(queue) == 0:
        print(-1)
    else:
        print(queue[-1])

queue = deque()

N = int(input())

for i in range(N):
    order = input().strip()
    if order[0:4] == "push":
        X = int(order[4:])
        queue.append(X)
    elif order == "pop":
        pop(queue)
    elif order == "size":
        print(len(queue))
    elif order == "empty":
        empty(queue)
    elif order == "front":
        front(queue)
    else:
        back(queue)
