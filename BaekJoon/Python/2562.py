import sys

max = 0
index = 0

for i in range(9):
    num = int(sys.stdin.readline())
    if max < num:
        max = num
        index = i + 1

print(max)
print(index)
