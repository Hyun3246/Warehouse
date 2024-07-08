import sys
input = sys.stdin.readline

N = int(input())

numbers = [int(input()) for _ in range(N)]

numbers.sort()

print(round(sum(numbers) / len(numbers)))
print(numbers[N//2])

num_dict = dict()

for i in numbers:
    if i in num_dict:
        num_dict[i] += 1
    else:
        num_dict[i] = 1
        
max_number = max(num_dict.values())
max_dict = []

for i in num_dict:
    if max_number == num_dict[i]:
        max_dict.append(i)

if len(max_dict) > 1:
    print(max_dict[1])
else:
    print(max_dict[0])


print(max(numbers) - min(numbers))
