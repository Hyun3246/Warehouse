import sys
input = sys.stdin.readline

def insert_stack(stack, a):
    stack.append(a)

def delete_one(stack):
    if len(stack) == 0:
        print(-1)
    else:
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

K = int(input())

for i in range(K):
    order = int(input())
    
    if order == 0:
        delete_one(stack)
    else:
        insert_stack(stack, order)


print(sum(stack))
