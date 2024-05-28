import sys
input = sys.stdin.readline

def insert_stack(stack, a):
    stack.append(a)

def delete_one(stack):
    if len(stack) == 0:
        print(-1)
    else:
        print(stack[-1])
        stack.pop(-1)

def stack_length(stack):
    print(len(stack))

def stack_empty(stack):
    if len(stack) != 0:
        print(0)
    else:
        print(1)

def latest_one(stack):
    if len(stack) != 0:
       print(stack[-1])
    else:
        print(-1)

stack = []

N = int(input())

for i in range(N):
    order = 0
    order = list(map(int, input().split()))

    if order[0] == 1:
        insert_stack(stack, order[1])
    elif order[0] == 2:
        delete_one(stack)
    elif order[0] == 3:
        stack_length(stack)
    elif order[0] == 4:
        stack_empty(stack)
    else:
        latest_one(stack)
