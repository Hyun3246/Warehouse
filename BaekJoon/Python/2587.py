import sys

numbers = []

for i in range(5):
    num = int(sys.stdin.readline().strip())
    numbers.append(num)

numbers.sort()

print(sum(numbers)//len(numbers))
print(numbers[2])
