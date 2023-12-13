N = int(input())
num_list = list(map(int, input().split()))

max = -1000001
min = 1000001

for i in num_list:
    if max < i:
        max = i
    if min > i:
        min = i

print(min, max)
