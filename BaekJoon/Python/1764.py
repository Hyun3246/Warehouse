import sys

name_set_1 = set()

N, M = map(int, sys.stdin.readline().strip().split())
for i in range(N):
    name = sys.stdin.readline().strip()
    name_set_1.add(name)

name_set_2 = set()

for i in range(N):
    name = sys.stdin.readline().strip()
    name_set_2.add(name)

name_set_3 = set.intersection(name_set_1, name_set_2)

name_list = list(name_set_3)
name_list.sort()

print(len(name_list))
for i in name_list:
    print(i)
