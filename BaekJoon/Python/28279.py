import sys
from collections import deque
input = sys.stdin.readline

def append(queue, X, position):
    if position == 1:
        queue.appendleft(X)
    else:
        queue.append(X)

def pop(queue, position):
    if len(queue) == 0:
        print(-1)
    else:
        if position == 3:
            print(queue[0])
            queue.popleft()
        else:
            print(queue[-1])
            queue.pop()

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

for _ in range(N):
    order = list(map(int, input().split()))
    if order[0] == 1 or order[0] == 2:
        append(queue, order[-1], order[0])
    elif order[0] == 3 or order[0] == 4:
        pop(queue, order[0])
    elif order[0] == 5:
        print(len(queue))
    elif order[0] == 6:
        empty(queue)
    elif order[0] == 7:
        front(queue)
    else:
        back(queue)
