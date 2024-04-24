import sys

N = sys.stdin.readline().strip()

num_list = []

for i in N:
    num_list.append(int(i))

num_list.sort(reverse=True)

for i in num_list:
    print(i, end="")
