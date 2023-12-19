import sys

N = int(sys.stdin.readline().rstrip())
numbers = sys.stdin.readline().rstrip()

number_list = []

for i in range(N):
    number_list.append(int(numbers[i]))
    
print(sum(number_list))
