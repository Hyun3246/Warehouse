import sys
input = sys.stdin.readline

N = int(input())

numbers = list(map(int, input().split()))

answer = sorted(numbers)

stack = []

result = []

current = 1

while current <= N:
    if (len(numbers) != 0) and (numbers[0] == current):
        result.append(numbers[0])
        numbers.pop(0)
        current += 1

    else:
        if (len(stack) != 0) and (stack[-1] == current):
            result.append(stack[-1])
            stack.pop()
            current += 1


        else:
            if len(numbers) == 0:
                break
            else:
                stack.append(numbers[0])
                numbers.pop(0)



        

if result == answer:
    print("Nice")
else:
    print("Sad")
